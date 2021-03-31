# Diff Checker Shell Script (pass in URL as args)
python3 hw3.py $1 > "$0.hw3-test.html"
curl --silent $1 > "$0.curl-test.html"
diff -y --suppress-common-lines "$0.hw3-test.html" "$0.curl-test.html"
rm "$0.hw3-test.html" "$0.curl-test.html"