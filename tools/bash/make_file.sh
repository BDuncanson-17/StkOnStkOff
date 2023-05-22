alias_exists() {
  local alias_name=$1

  # Check if the alias exists in the current shell session
  if alias | grep -wq "$alias_name"; then
    return 0  # Alias exists
  else
    return 1  # Alias does not exist
  fi
