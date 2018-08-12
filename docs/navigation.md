# Navigation Patterns

The following table defines all Navigation Patterns for Web UI discovering.

| Patterns                     | New Page | Anchor   | Modal    | Link     | Button   | Input    | JS       |      |
| ---------------------------- | -------- | -------- | -------- | -------- | -------- | -------- | -------- | ---- |
| Link `<a>`                   | yes      | yes      | yes      | no       | no       | No       | no       |      |
| Button `<button>`            | yes      | yes      | yes      | yes      | no       | yes      | optional |      |
| Input `<input>` `<textarea>` | no       | no       | no       | no       | yes      | yes      | optional |      |
| Div `<div>`                  | yes      | yes      | yes      | yes      | yes      | yes      | required |      |
| Image <image>                | no       | no       | no       | no       | no       | no       | required |      |
| iframe                       | N/A      | N/A      | N/A      | N/A      | N/A      | N/A      | optional |      |
| canvas                       | N/A      | N/A      | N/A      | N/A      | N/A      | N/A      | required |      |
| any others                   | possible | possible | possible | possible | possible | possible | required |      |

## Problems

- Ajax response navigations
- Input and then click something
  - explain input field to user
  - show sereies of inputs
- Dealing with webpacked website (or SPA)
  - simulating all clicks
- Use Same origin policy to creep the site, and stop on the last link

Key-text-nav

## next steps

- should suitable for multiple website as arguments
- news / blogs / content aggregations / shopping
- websites contains series of actions / interactive
- demo for websites
- labeling intermediate state
- online-labeling tool
- present / parse labels for each actions 


## community discover and learn from community

- looking for the most important node
- summarise the website
- structure learning, site structre as input, 
- center of the community
- simple filtering
- community as input, find community by algorithm
- paper reading

```
{
    "id": 1,
    "type": "link",
    "value": "",
    "description": "",
    "is_end": true,
    "next": []
}
```

