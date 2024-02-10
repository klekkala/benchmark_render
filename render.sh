
if [ $# -eq 0 ]; then
  echo "Error: Please provide an argument."
  exit 1
fi

for entry in "/lab/tmpig10b/kiran/splat_files/$1/"*; do
    #python /lab/tmpig10c/kiran/nerf/GNerf/gaussian-splatting/render.py -m "$entry"
    python ./gaussian-splatting/render.py -m "$entry"
  done



