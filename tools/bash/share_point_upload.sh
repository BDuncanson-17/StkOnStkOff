#!/bin/bash

# Function to display usage and help
display_usage() {
    echo "This script uploads a file to my sharepoint for late user"
    echo "Parameters:"
    echo "    username                SharePoint username."
    echo "    password                SharePoint password."
    echo "    sharepoint_server       SharePoint server URL."
    echo "    site_name               SharePoint site name."
    echo "    folder_relative_url     Relative URL of the folder (from the site root)."
    echo "    filename                Name of the file to upload."
    echo "    local_file_path         Local path of the file to upload."
}


read -p "Enter username: " username
read -p "Enter password: " password
sharepoint_server="3tmh0v.sharepoint.com"
site_name="bds_ad"
folder_relative_url="bds_ad/bds_docs"
filename='./file.txt'


# Make the POST request using curl
# Using NTLM authentication (--ntlm) with the provided username and password (--user "$username:$password")
# File data is sent in binary format (--data-binary "@$local_file_path")
# The request's content type is set to application/octet-stream (--header "Content-Type: application/octet-stream")
# The URL is constructed using the provided parameters
curl -X POST \
    --ntlm \
    --user "$username:$password" \
    --data-binary "@$local_file_path" \
    --header "Content-Type: application/octet-stream" \
    "https://$sharepoint_server/sites/$site_name/_api/web/getfolderbyserverrelativeurl('$folder_relative_url')/files/add(url='$filename', overwrite=true)"