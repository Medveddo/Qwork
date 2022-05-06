# Telnet inside alpine container

`apk --update --no-cache add busybox-extras`

`busybox-extras telnet localhost 80`

## Delete zinc index

```bash
curl -X DELETE \
  'https://zinc.qwork.sizikov.space/api/index/:_index_name' \
  --header 'Accept: */*' \
  --header 'Authorization: Basic base64(user:password)'
```
