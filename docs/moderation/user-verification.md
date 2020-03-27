---
description: >-
  Lets users verify themselves before they can join your server. You can
  implement several verification methods.
---

# User Verification

## ;verification

Primary command to setup several verification methods.

### role

Set the role which will be assigned to unverified members to keep them locked away from accessing normal

```yaml
Usage:
;verification role <role>
```

#### remove

Removes the verification role hence disabling all of the verification methods from the server.

```yaml
;verification role remove
```

### reaction

Primary command for reaction verification method.

#### set

Set react to verify method to authenticate users to your server.
You can specify the message ID or message URL if you want this reaction to be added over a custom message otherwise the default embed is used for the same. The emote you want to use for reacting, custom URLs for

```yaml
Aliases:
- setup

Usage:
;verification reaction set [message] [channel] [emote] [icon_url] [image_url] [description]
```

#### remove

Removes the reaction verification method from the server.

```yaml
Aliases:
- delete

Usage:
;verification reaction remove
```
