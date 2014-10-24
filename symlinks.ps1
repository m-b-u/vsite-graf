# Based on this answer on stack overflow: http://stackoverflow.com/a/5930443/18475

# Get list of all symlinks in repository
$symlinks = &git ls-files -s | gawk '/120000/{print $4}'
foreach ($symlink in $symlinks) {
	# Output symlink
	write-host $symlink

	# Check if symlink is not yet a real symlink to not mess with good symlinks
	$file = Get-Item $symlink -Force -ea 0
	If (!([bool]($file.Attributes -band [IO.FileAttributes]::ReparsePoint)))
	{
		# Get symlink path
		$content = [IO.File]::ReadAllText($symlink)
		# Delete file that is placed instead of symlink
		Remove-Item $symlink
		# Adjust slashes in path to conform to what mklink expects
		$adjustedSource = $symlink.replace("/", "\")
		$adjustedTarget = $content.replace("/", "\")
		# Create symlink
		cmd /c mklink "$adjustedSource" "$adjustedTarget"
	}
	
	# Mark symlink as not changed to not confuse git
	&git update-index --assume-unchanged $symlink
}