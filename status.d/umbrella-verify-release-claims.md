**Target:** embarch-release-signing-proposal.md — step 3 paragraph (line 25), the "**Still proposed:**" sentence
**Was:** "**Still proposed:** checking the certificate's source-repository and ref extensions against that identity too (the identity already names both), and a test against a real suite release bundle, which needs step 1 first."
**Now:** Remove the first half: verify-release checks the Source Repository URI, Ref and Build Config URI extensions as exact strings (EMB-343, umbrella/108). Keep only "a test against a real suite release bundle, which needs step 1 first."
