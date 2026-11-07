"""Align LTXConditionPipeline's per-token stochastic step with Lightricks.

Diffusers 0.42.1's LTXConditionPipeline negates the model velocity before calling
its scheduler. This is correct for that scheduler's per-token Euler branch,
whose dt is current_sigma-next_sigma, but its stochastic branch expects the
original velocity. The latter otherwise estimates x0 with the opposite sign.

Source comparisons:
https://github.com/Lightricks/LTX-Video/blob/main/ltx_video/schedulers/rf.py
https://github.com/huggingface/diffusers/blob/v0.42.1/src/diffusers/pipelines/ltx/pipeline_ltx_condition.py
https://github.com/huggingface/diffusers/blob/v0.42.1/src/diffusers/schedulers/scheduling_flow_match_euler_discrete.py

An exact last-step numerical probe detects whether the installed library needs
the correction. A future library that already matches the reference is left
alone; any third behavior fails loudly.
"""
import torch
from diffusers import FlowMatchEulerDiscreteScheduler


def probe_per_token_stochastic_sign():
    base=FlowMatchEulerDiscreteScheduler(shift=1.0,use_dynamic_shifting=False,
                                        stochastic_sampling=True)
    base.set_timesteps(timesteps=[421.9],sigmas=[0.4219])
    sample=torch.tensor([[[2.0]]])
    velocity=torch.tensor([[[0.5]]])
    expected=sample-0.4219*velocity
    actual=base.step(-velocity,torch.tensor(421.9),sample,
        per_token_timesteps=torch.tensor([[421.9]]),return_dict=False,
        generator=torch.Generator().manual_seed(0))[0]
    wrong_sign=sample+0.4219*velocity
    if torch.allclose(actual,expected,atol=1e-6):needed=False
    elif torch.allclose(actual,wrong_sign,atol=1e-6):needed=True
    else:raise RuntimeError('Unexpected stochastic scheduler behavior; recheck the reference implementation')
    return {'fix_required':needed,'reference_x0':float(expected.item()),
            'unmodified_diffusers_x0':float(actual.item())}


class LTXPerTokenStochasticScheduler(FlowMatchEulerDiscreteScheduler):
    def step(self,model_output,timestep,sample,**kwargs):
        if self.config.stochastic_sampling and kwargs.get('per_token_timesteps') is not None:
            if not hasattr(self,'_ltx_sign_fix_required'):
                self._ltx_sign_fix_required=probe_per_token_stochastic_sign()['fix_required']
            if self._ltx_sign_fix_required:model_output=-model_output
        return super().step(model_output,timestep,sample,**kwargs)


def validate_corrected_step():
    result=probe_per_token_stochastic_sign()
    corrected=LTXPerTokenStochasticScheduler(shift=1.0,use_dynamic_shifting=False,
                                             stochastic_sampling=True)
    corrected.set_timesteps(timesteps=[421.9],sigmas=[0.4219])
    value=corrected.step(torch.tensor([[[-0.5]]]),torch.tensor(421.9),torch.tensor([[[2.0]]]),
        per_token_timesteps=torch.tensor([[421.9]]),return_dict=False,
        generator=torch.Generator().manual_seed(0))[0]
    result['corrected_x0']=float(value.item())
    result['matches_reference']=abs(result['corrected_x0']-result['reference_x0'])<1e-6
    if not result['matches_reference']:raise RuntimeError('Corrected scheduler failed reference comparison')
    cases=[]
    for stochastic,per_token,conditioned in [(False,True,False),(True,False,False),(True,True,True)]:
        check=LTXPerTokenStochasticScheduler(shift=1.0,use_dynamic_shifting=False,
                                             stochastic_sampling=stochastic)
        check.set_timesteps(timesteps=[421.9],sigmas=[0.4219])
        model_output=torch.tensor([[[-0.5 if per_token else 0.5]]])
        kwargs={'return_dict':False,'generator':torch.Generator().manual_seed(0)}
        if per_token:kwargs['per_token_timesteps']=torch.tensor([[0.0 if conditioned else 421.9]])
        actual=check.step(model_output,torch.tensor(421.9),torch.tensor([[[2.0]]]),**kwargs)[0]
        expected=2.0 if conditioned else result['reference_x0']
        passed=abs(float(actual.item())-expected)<1e-6
        cases.append({'stochastic':stochastic,'per_token':per_token,'conditioned_sigma_zero':conditioned,
                      'value':float(actual.item()),'expected':expected,'passed':passed})
        if not passed:raise RuntimeError('A scheduler control case failed')
    result['control_cases']=cases
    # Cover a non-final step and both a noisy and an exactly conditioned token.
    # The terminal-step probe above deliberately removes noise; this one also
    # checks the stochastic interpolation against the native RF equation.
    mixed=LTXPerTokenStochasticScheduler(shift=1.0,use_dynamic_shifting=False,
                                         stochastic_sampling=True)
    mixed.set_timesteps(timesteps=[725.0,421.9],sigmas=[0.725,0.4219])
    sample=torch.tensor([[[2.0],[3.0]]])
    velocity=torch.tensor([[[0.5],[0.8]]])
    current=torch.tensor([[[0.725],[0.0]]])
    following=torch.tensor([[[0.4219],[0.0]]])
    noise=torch.randn(sample.shape,generator=torch.Generator().manual_seed(17))
    expected=(1.0-following)*(sample-current*velocity)+following*noise
    actual=mixed.step(-velocity,torch.tensor(725.0),sample,
        per_token_timesteps=current.squeeze(-1)*1000,return_dict=False,
        generator=torch.Generator().manual_seed(17))[0]
    error=float((actual-expected).abs().max())
    result['mixed_tokens_nonfinal_step']={'max_abs_error':error,'passed':error<1e-6,
        'actual':actual.flatten().tolist(),'reference':expected.flatten().tolist()}
    if error>=1e-6:raise RuntimeError('Non-final stochastic interpolation failed reference comparison')
    return result
