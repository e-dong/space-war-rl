At work I learned the power of automation and how it saves valuable time and increase value throughput to stakeholders. Since I'm starting to do deployments to itch.io, I can apply the same principle. I've only used gitlab ci, so this will be my first time using github actions. Other than syntax differences, the main difference is the paradigm to accomplish similar things.

Before automating something, it is important to determine what the manual steps are.

## Manual Steps

1. Execute `pygbag` + `args` to create a HTML archive
1. Navigate to the edit game page on itch.io
1. upload the archive and save the game page

## Automated Setup

Github offers a free CI/CD platform called [Github Actions](https://docs.github.com/en/actions). I can leverage this to automate the manual steps in a workflow. Workflows can be configured from yaml files. Github looks for these files in `.github/workflows`. The workflow files can be named anything, but should be relevant to the goal I'm trying to accomplish. I created a `deploy.yaml`, since my goal is to automate deployment to itch.io.

I will be using a third party github action extension called [itch-publish](https://github.com/KikimoraGames/itch-publish) from the github marketplace. This extension uses a docker image with butler installed to push my builds to itch.io.
