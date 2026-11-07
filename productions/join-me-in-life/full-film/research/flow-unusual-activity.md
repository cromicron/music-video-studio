# Flow unusual-activity failure: supported recovery

Checked **7 November 2026**, public official sources only. No account calls, generation retries, browser runs, network changes or spending by this researcher.

**Finding:** Google documents this exact failure and a normal delayed retry. It does not identify the specific cause or certify third-party CDP automation. Treat the first failure as an access/execution failure, not evidence against the hospital prompt or Veo's acting quality.

## Observed versus documented

Root reports that the first hospital submission failed immediately with no output. The UI said: “Fehlgeschlagen Wir haben ungewöhnliche Aktivitäten festgestellt. Beachten Sie, dass Browsererweiterungen, die die Seite verändern, Probleme verursachen können. Weitere Informationen finden Sie in der Google Flow-Hilfe.” This is a root-observed UI message, not independently reproduced here. Root is reconciling the balance; this report makes no debit/refund claim.

The session uses TinyFish's supported profile-setup REST/CDP interface, Chrome 147 and a managed proxy. Root reports no extension intentionally modifying the page. TinyFish's supported interface does **not** establish Google's support for that browser path. The error's extension warning is generic; it does not prove an extension was present or responsible.

## Official guidance

[Google Flow Help, English](https://support.google.com/flow/answer/16353333?hl=en), also [German](https://support.google.com/flow/answer/16353333?hl=de), has a specific unusual-activity section: **“Retry after a couple of minutes.”** It also instructs disabling VPNs/proxies. The page recommends desktop Chromium and warns that other browsers may behave unexpectedly. It states that failed-generation credits are returned within one hour; balance and history can update at different times. Its refresh advice concerns initially missing generation records, not a documented cure for unusual activity.

[Google's reporting instructions](https://support.google.com/flow/answer/16353335?hl=en) provide **More → Send app feedback**, with a screenshot, and link Google One support for access issues in supported regions. These are documented escalation routes, not permission for this researcher to send a report.

[Google Terms of Service](https://policies.google.com/terms?hl=en), retrieved version effective **30 July 2026** (US page), prohibit bypassing protective measures and automated content access contrary to machine-readable instructions. This wording is not a blanket endorsement or blanket prohibition of all browser control. The reviewed Flow help does not specifically approve TinyFish/CDP or establish that this failure means automation is categorically forbidden. [Flow's documented built-in Agent](https://support.google.com/flow/answer/17093911?hl=en) is a separate first-party feature; it is not evidence that switching to it would avoid this error.

## Bounded next step for root

1. Keep the failed card/error, timestamp, source hashes and settings; reconcile balance. Preserve uncertainty about the cause. Do not alter the artistic prompt to solve this error.
2. Google's delay makes **one deliberate retry after a few minutes** a documented recovery option, subject to root's remaining attempt/credit budget and decision. No retry was performed here. Do not turn this into polling or repeated generation.
3. The managed proxy is a concrete possible mismatch with the help guidance, not a proven diagnosis. **Do not modify/rotate proxies, spoof fingerprints, change identity, export cookies or create accounts.** This report does not recommend any such change.
4. If the same failure persists, stop submissions in this path. Use Google's feedback/support route. An ordinary interactive desktop Chrome session on the user's existing normal connection is consistent with Google's documented browser/network guidance; it is an untested legitimate fallback, not guaranteed recovery. Do not migrate the automated session merely to evade the signal.

**Remaining unknown:** whether this was transient, network-related, extension/interference-related, or an unsupported automated-browser context; actual charge/refund; whether any ordinary documented recovery succeeds. Refresh alone, cookie clearing, a specific cooldown beyond Google's couple-of-minutes guidance, and an alleged device “trust score” are not verified remedies for this case.
