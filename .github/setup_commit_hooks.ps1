# Setup commit message hooks for the repository

# Create the hooks directory if it doesn't exist
if (!(Test-Path -Path ".git/hooks")) {
    New-Item -ItemType Directory -Path ".git/hooks" -Force
}

# Create the commit message hook
$hookContent = @'
#!/bin/bash
# Commit message hook to enforce conventional commits

commit_msg_file=$1
commit_msg=$(cat $commit_msg_file)

# Check if commit message follows conventional commits format
if ! echo "$commit_msg" | grep -qE "^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)(\(.+\))?: .+"; then
    echo "❌ Invalid commit message format"
    echo "Commit message must follow the Conventional Commits specification:"
    echo "  <type>(<scope>): <subject>"
    echo ""
    echo "Valid types:"
    echo "  build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test"
    echo ""
    echo "Examples:"
    echo "  feat(parser): add support for concurrent document processing"
    echo "  fix(cli): correct argument parsing for output directory"
    echo "  docs(readme): update usage instructions"
    echo ""
    echo "See docs/contributing.md for more details."
    exit 1
fi

echo "✅ Commit message format is valid"
exit 0
'@

Set-Content -Path ".git/hooks/commit-msg" -Value $hookContent

# Make the hook executable (this works on Windows with Git Bash)
# We don't need to set executable permissions on Windows

Write-Host "✅ Commit message hook installed successfully"
Write-Host "Commit messages will now be validated against the Conventional Commits specification"