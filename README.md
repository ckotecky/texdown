Merge:
- `texdown -m True -i path -o merged.md -st 3`
- `texdown --merge True --input path --output merged.md --strip_top 3`

Convert:
- `texdown -c True -i merged.md -o .`
- `texdown --convert True --input merged.md --output .`

Merge & Convert:
- `texdown -c True -m True -i path -o .`
- `texdown --convert True --merge True --input path --output .`


