# cli-browser
A tool to browse CLIs like AWS.
Currently when you start the script, you will see all your ECS clusters and will be able to navigate through it with the directional arrows:
- Left: go back
- Right: explore the data highlighted by the cursor. (For example if your cursor is on a specific cluster, you will see all the services in that cluster)
- Up: Scroll up through the elements
- Down: Scroll down through the elements

## But why?
I was tired of using the AWS CLI and copy pasting ARNs around to check what's deployed and so on, and I feel like the Console is too slow. 

## Usage
`python CliBrowser.py`

So far only the browsing of some features in ECS have been implemented (see `EcsManager.py``).

The code is decoupled in a way that it can be reused to browse other services in AWS, or even other types of CLI. Maybe Kubernetes in the future.

The main calls a "Data Manager" (only ECS for now), which is responsible to fetch the data.
This Data Manager uses a "Data Handler" (only JSON Handler for now, since ECS returns JSON) to handle the data.
The Data Manager uses a `Navigator` which is responsible for the navigation of the user through the data.
Finally the Navigator uses the `Display` to display the data.

This architecture allows me to reuse the JSON Handler for other CLIs that return JSON formatted data.

## What's next
- Adding other services from AWS to browse (S3 for ex.)
- Adding other CLIs (Kubernetes for ex.)
- Implement a search
- Fix bugs
