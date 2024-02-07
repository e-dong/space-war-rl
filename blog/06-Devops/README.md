At work I learned the power of automation and how it saves valuable developer time. Since I'm starting to do deployments to itch.io, I can apply the same principle. I've only used gitlab ci, so this will be my first time using github actions. Other than syntax differences, the main difference is the paradigm to accomplish similar things.

## Manual Steps

These are the steps I take without automation.

1. Execute `pygbag` + `args` to create a HTML archive
1. Navigate to the edit game page
1. upload the archive and save the game

## Automated Setup

Github offers a free CI/CD platform called [Github Actions](https://docs.github.com/en/actions). I can leverage this to automate the manual steps.

I will be using a third party github action extension called [itch-publish](https://github.com/KikimoraGames/itch-publish) from the github marketplace.
