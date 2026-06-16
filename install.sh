echo "Pull updates"
git pull

echo "Clean installed package"
pip uninstall pydme

echo "Install new package"
pip install -e .
