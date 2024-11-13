# ispy-readii
Running READII to perform radiomic feature extraction on the I-SPY cohort for radiogenomic analysis.

## Development

### Installing Pixi

Pixi is a tool for managing conda environments and managing dependencies. 

To install pixi, visit the [pixi website](https://pixi.sh/) and follow the instructions for your operating system.

### Cloning the repository

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/bhklab/RECIST-play.git
```

### Installing dependencies

To install the dependencies for the handbook, run the following command:

```bash
pixi install
```

This will install the dependencies specified in the `pixi.toml` file.

### Adding dependencies

To add a new dependency, run the following command:

```bash
pixi add <package_name>
```

This will add the specified package to the `pixi.toml` file.


## Directory Structure
Run the following command in your terminal in the ispy-readii directory to set up the project directory structure:
```shell
mkdir -p procdata rawdata results workflow/{config,envs,logs,notebooks,scripts}
```

You should now have the following directory structure:
```bash
├── README.md
├── procdata        # output from any processing steps of rawdata
├── rawdata         # data as it is downloaded from the source
├── results         # final output from the pipeline
└── workflow
    ├── config
    ├── envs
    ├── logs
    ├── notebooks   # Jupyter, R notebooks
    └── scripts     # Where any code scripts are kept (Python, R, etc.)
```


## Contributing

Please use the following angular commit message format:
```
<type>(optional scope): short summary in present tense

(optional body: explains motivation for the change)

(optional footer: note BREAKING CHANGES here, and issues to be closed)

```
`<type>` refers to the kind of change made and is usually one of:

- `feat`: A new feature.
- `fix`: A bug fix.
- `docs`: Documentation changes.
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc).
- `refactor`: A code change that neither fixes a bug nor adds a feature.
- `perf`: A code change that improves performance.
- `test`: Changes to the test framework.
- `build`: Changes to the build process or tools.

`scope` is an optional keyword that provides context for where the change was made. It can be anything relevant to your package or development workflow (e.g., it could be the module or function - name affected by the change).