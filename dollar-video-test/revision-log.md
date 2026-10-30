# Revision log

| Change | Before evidence | After evidence | Recheck / remaining coverage |
|---|---|---|---|
| Avoid a visually empty headline on the first frame after a scene cut. | `qa/before-cut-frame85.png` is a decoded frame from the first render: the second scene's title was invisible at frame 85. | `qa/after-cut-frame85.png` is decoded from the final render: the title is visible immediately at frame 85. | The final decoded contact sheet includes neighboring frames 84–85, 194–195 and 301–302. This establishes selected-frame visibility only; complete playback/pacing remains NOT CHECKED. |
| Do not announce the new network connection before the participant appears. | Earlier renderer displayed “A CAN CONNECT WITH D” from the first frame of the network scene. The complete earlier render was not retained; baseline frame evidence for this change is NOT CHECKED. | The text is now gated until frame 270 (scene-local frame 75); the final contact sheet includes frame 260 without the text and frame 301 with it. | Selected-frame check only; no claim of full semantic audience validation. |
