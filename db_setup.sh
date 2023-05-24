#!/bin/bash
# Check if the 'data' directory exists, otherwise create it
if [ ! -d "./data" ]; then
    mkdir -p "./data"
fi

# Append strings to the database files
cat > ./data/stack-template-map.db << EOF
webpdf-webpdf-vpc/home/bryan/Documents/stkonstkoff/data/cached_templates/webpdf-vpc.yaml
webpdf-web/home/bryan/Documents/stkonstkoff/data/cached_templates/webpdf-web.yaml
webpdf-security/home/bryan/Documents/stkonstkoff/data/cached_templates/webpdf-security.yaml
EOF

cat > ./data/template_paths.db << EOF
/home/bryan/Documents/stkonstkoff/data/cached_templates/webpdf-vpc.yaml
/home/bryan/Documents/stkonstkoff/data/cached_templates/webpdf-web.yaml
/home/bryan/Documents/stkonstkoff/data/cached_templates/webpdf-security.yaml
EOF


echo "webpdf-" > "./data/prefix_strings.db"

# Inform that the script is for setting up the database
echo "Database setup completed successfully."
