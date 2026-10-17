# Free Flightdeck cockpit content updates

`cockpit-v1.json` is the public, data-only update channel for apps supporting `cockpit-models-v1`. Users choose Downloads / updates → Check for updates → Update. Only changed packs download; existing verified content remains usable until installation succeeds. Installed content and the checked catalog work offline.

Publish immutable `.fdpack` archives in a GitHub Release first. Reuse unchanged pack entries; give each changed archive a new version and checksum. Increment the channel sequence on every catalog change. Never overwrite an existing archive/version or reuse a sequence. Keep every required baseline pack and file. Do not change node names, control bindings, mounting coordinates, material semantics or other runtime contracts on this channel. Incompatible changes need corresponding app support and a new compatibility channel.

In the Flightdeck source workspace, `scripts/prepare-content-update.py --catalog <candidate.json> --sequence <next-number> --previous <previous-channel.json> --output <new-channel.json>` verifies all public archive sizes/checksums and validates the catalog before publication. Publish the resulting JSON here only after those checks pass. The initial sequence is 1 and has no previous file.

New independent complete models may use a `panel-...` pack containing GLBs with `modelId` and a `component` object with `title` and `description`. `scripts/build-inspection-content-pack.py` prepares these without changing the original geometry. They appear in the complete-component inspector, with front/rear/side views. This does not automatically place them in the installed cockpit or invent control behavior. Follow the owner's real-aircraft reference, complete-assembly and review requirements before publishing new geometry.

Downloads contain only model/image data and manifests, never remote application code. The custom MCDU stays bundled and is excluded from this channel. No paid hosting service is required.
