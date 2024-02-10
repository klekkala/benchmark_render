if [ $# -eq 0 ]; then
  echo "Error: Please provide an argument."
  exit 1
fi


for entry in "/lab/tmpig10b/kiran/gs_train/$1/"*; do
    echo $entry
    folder_name=$(basename "$entry")
    python3 /lab/tmpig10c/kiran/nerf/GNerf/gaussian-splatting/train.py -s "$entry" -m "/lab/tmpig10b/kiran/splat_files/$1/$folder_name"
  done
