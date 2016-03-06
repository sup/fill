echo "Cleaning app directories..."
find . -name "*.pyc" -exec rm -rf {} \;
echo "Done."
echo "Starting dev server..."
dev_appserver.py fill-app/
