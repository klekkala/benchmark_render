import subprocess

def convert_colmap_model(input_path="/lab/kiran/navisim/haopeng/data/colmap/TXT", output_path="/lab/kiran/navisim/haopeng/data/colmap/BIN", output_type="BIN"):
    """
    Converts a COLMAP model between different formats.

    :param input_path: Path to the source COLMAP model folder (e.g., TXT folder).
    :param output_path: Path to the destination folder for the converted model (e.g., BIN folder).
    :param output_type: Desired output format (BIN or TXT).
    """
    command = [
        "colmap",
        "model_converter",
        "--input_path", input_path,
        "--output_path", output_path,
        "--output_type", output_type
    ]

    # Run the command and raise an error if it fails
    subprocess.run(command, check=True)
    print(f"Model converted from {input_path} to {output_path} in {output_type} format.")

if __name__ == "__main__":
    convert_colmap_model()
