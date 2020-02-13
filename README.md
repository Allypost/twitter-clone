# Twitter Clone
This is a simple Twitter clone written in Python and Vue.

The frontend and backend are fully decoupled by design.



## How to start

### Mac/Linux
The project requires `docker` and `docker-compose` with support for running `docker` commands without `sudo`.

#### General
  1. Run `make init` to create an `.env` file, register git hooks, and build and start the application
  2. (Optional) Update the new `.env` if needed

#### Development
  1. Do steps outlined in [General](#General)
  2. Update the `.env` file and set `APP_SETTINGS` to `config.DevelopmentConfig`
  3. Run `make watch` to start frontend asset watcher.
     It should also auto-reload the server after each build to refresh frontend assets.
  4. Run `make refresh-backend` to restart the backend when needed
  5. Run `make lint` periodically to lint the project (and auto-fix some issues)
  6. After updating models run `make migration` to create a migration and `make migrate` to apply migrations to database

### Windows
Run it in a linux VM or on a linux server and see [Mac/Linux](#Mac/Linux)

## Make commands/targets

The Makefile contains many useful commands (or targets).

|      Command      |                   Description                     |
|-------------------|---------------------------------------------------|
| `init`            | Initialise project (should be run only once)      |
| `up`              | Create and start containers                       |
| `down`            | Stop and remove containers                        |
| `restart`         | Alias for `make down && make up`                  |
| `up-db`           | Create and start the database container           |
| `prod`            | Command to set-up production build                |
| `dev`             | Convenience command for development. Starts containers, runs asset watcher and shuts down containers when watcher exists |
| `watch`           | Run frontend asset watcher/builder                |
| `refresh-backend` | Restart backend application                       |
| `build`           | Build all assets                                  |
| `lint`            | Lint (check) and fix files                        |
| `shell`           | Attach flask shell to currently running app       |
| `migration`       | Create a new migration. Automatically detects required changes from models and current database schema. |
| `migrate`         | Apply migrations to database                      |
| `migrate-down`    | Remove last migration from database               |
| `containers-build`| Build docker containers                           |

They can all run as `make <command>` 



## docker(-compose) helpers
The application contains several helper scripts for using `docker`.
They are all located in the `docker` folder and the scripts are intended to
be used as an alias for commands that are required to develop the application.

For example, if a new `pip` package is required, instead of running
`pip install package_name`, it should be run as `docker/pip install package_name`.
This ensures that everything is set up right and the `requirements.txt` file is updated.

The whole list with a brief description:

|      Command      |                   Description                     |
|-------------------|---------------------------------------------------|
| `pip`             | `pip` alias                                       |
| `yarn`            | `yarn` alias                                      |
| `python`          | `python` alias                                    |
| `frontend`        | Run a command in the `frontend` (node) container  |
| `backend`         | Run a command in the `backend` (python) container |
| `run`             | Run a command in a container                      |

They can all be run as `docker/<command> <arg>...`, or rather, they should be treated as an alias for the actual command.
Eg. commands starting with `pip` should be replaced with `docker/pip` and so on.
