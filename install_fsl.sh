#!/bin/bash

echo "Starting FSL installation and setup..."

# Ensure Conda is installed
if ! command -v conda &> /dev/null; then
    echo "Error: Conda is not installed. Install Anaconda or Miniconda first."
    exit 1
fi

# Add FSL Conda channel and set priority
conda config --add channels https://fsl.fmrib.ox.ac.uk/fsldownloads/fslconda/public/
conda config --set channel_priority strict

# Create the Conda environment
echo "Creating Conda environment: fsl-env"
conda create -y -n fsl-env -c fsl -c conda-forge \
    python=3.11 fsl-base fslpy numpy scipy nibabel h5py pyyaml ruamel.yaml jupyterlab ipykernel

# Activate the environment
echo "Activating fsl-env..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate fsl-env

# Setup FSL environment variables
echo "Configuring FSL environment..."
mkdir -p "$CONDA_PREFIX/etc/conda/activate.d" "$CONDA_PREFIX/etc/conda/deactivate.d"

cat <<EOF > "$CONDA_PREFIX/etc/conda/activate.d/fsl_activate.sh"
export FSLDIR=\$CONDA_PREFIX
source \$FSLDIR/etc/fslconf/fsl.sh
export PATH=\$FSLDIR/bin:\$PATH
export FSLOUTPUTTYPE=NIFTI_GZ
EOF

cat <<EOF > "$CONDA_PREFIX/etc/conda/deactivate.d/fsl_deactivate.sh"
unset FSLDIR
unset FSLOUTPUTTYPE
EOF

chmod +x "$CONDA_PREFIX/etc/conda/activate.d/fsl_activate.sh" "$CONDA_PREFIX/etc/conda/deactivate.d/fsl_deactivate.sh"

# Install additional Python dependencies
echo "Installing additional Python dependencies..."
pip install -q "readii>=1.16.0,<2" "med-imagetools" "scikit-image>=0.19.0"

# Register Jupyter kernel as "fsl-env"
echo "Registering Jupyter kernel..."
python -m ipykernel install --user --name fsl-env --display-name "fsl-env"

# Verify FSL installation
echo "Verifying FSL installation..."
if ! command -v fast &> /dev/null; then
    echo "Warning: 'fast' command not found. Try restarting your terminal or running 'source ~/.bashrc'"
    exit 1
fi

echo " FSL installation completed successfully."
echo "To use FSL, run: conda activate fsl-env"
