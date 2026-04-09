import{ShellCompDirective as e}from"./index.mjs";function t(t,n){return`#compdef ${t}
compdef _${t} ${t}

# zsh completion for ${t} -*- shell-script -*-

__${t}_debug() {
    local file="$BASH_COMP_DEBUG_FILE"
    if [[ -n \${file} ]]; then
        echo "$*" >> "\${file}"
    fi
}

_${t}() {
    local shellCompDirectiveError=${e.ShellCompDirectiveError}
    local shellCompDirectiveNoSpace=${e.ShellCompDirectiveNoSpace}
    local shellCompDirectiveNoFileComp=${e.ShellCompDirectiveNoFileComp}
    local shellCompDirectiveFilterFileExt=${e.ShellCompDirectiveFilterFileExt}
    local shellCompDirectiveFilterDirs=${e.ShellCompDirectiveFilterDirs}
    local shellCompDirectiveKeepOrder=${e.ShellCompDirectiveKeepOrder}

    local lastParam lastChar flagPrefix requestComp out directive comp lastComp noSpace keepOrder
    local -a completions

    __${t}_debug "\\n========= starting completion logic =========="
    __${t}_debug "CURRENT: \${CURRENT}, words[*]: \${words[*]}"

    # The user could have moved the cursor backwards on the command-line.
    # We need to trigger completion from the $CURRENT location, so we need
    # to truncate the command-line ($words) up to the $CURRENT location.
    # (We cannot use $CURSOR as its value does not work when a command is an alias.)
    words=( "\${=words[1,CURRENT]}" )
    __${t}_debug "Truncated words[*]: \${words[*]},"

    lastParam=\${words[-1]}
    lastChar=\${lastParam[-1]}
    __${t}_debug "lastParam: \${lastParam}, lastChar: \${lastChar}"

    # For zsh, when completing a flag with an = (e.g., ${t} -n=<TAB>)
    # completions must be prefixed with the flag
    setopt local_options BASH_REMATCH
    if [[ "\${lastParam}" =~ '-.*=' ]]; then
        # We are dealing with a flag with an =
        flagPrefix="-P \${BASH_REMATCH}"
    fi

    # Prepare the command to obtain completions, ensuring arguments are quoted for eval
    local -a args_to_quote=("\${(@)words[2,-1]}")
    if [ "\${lastChar}" = "" ]; then
        # If the last parameter is complete (there is a space following it)
        # We add an extra empty parameter so we can indicate this to the go completion code.
        __${t}_debug "Adding extra empty parameter"
        args_to_quote+=("")
    fi

    # Use Zsh's (q) flag to quote each argument safely for eval
    local quoted_args=("\${(@q)args_to_quote}")

    # Join the main command and the quoted arguments into a single string for eval
    requestComp="${n} complete -- \${quoted_args[*]}"

    __${t}_debug "About to call: eval \${requestComp}"

    # Use eval to handle any environment variables and such
    out=$(eval \${requestComp} 2>/dev/null)
    __${t}_debug "completion output: \${out}"

    # Extract the directive integer following a : from the last line
    local lastLine
    while IFS='\n' read -r line; do
        lastLine=\${line}
    done < <(printf "%s\n" "\${out[@]}")
    __${t}_debug "last line: \${lastLine}"

    if [ "\${lastLine[1]}" = : ]; then
        directive=\${lastLine[2,-1]}
        # Remove the directive including the : and the newline
        local suffix
        (( suffix=\${#lastLine}+2))
        out=\${out[1,-$suffix]}
    else
        # There is no directive specified.  Leave $out as is.
        __${t}_debug "No directive found.  Setting to default"
        directive=0
    fi

    __${t}_debug "directive: \${directive}"
    __${t}_debug "completions: \${out}"
    __${t}_debug "flagPrefix: \${flagPrefix}"

    if [ $((directive & shellCompDirectiveError)) -ne 0 ]; then
        __${t}_debug "Completion received error. Ignoring completions."
        return
    fi

    local activeHelpMarker="%"
    local endIndex=\${#activeHelpMarker}
    local startIndex=$((\${#activeHelpMarker}+1))
    local hasActiveHelp=0
    while IFS='\n' read -r comp; do
        # Check if this is an activeHelp statement (i.e., prefixed with $activeHelpMarker)
        if [ "\${comp[1,$endIndex]}" = "$activeHelpMarker" ];then
            __${t}_debug "ActiveHelp found: $comp"
            comp="\${comp[$startIndex,-1]}"
            if [ -n "$comp" ]; then
                compadd -x "\${comp}"
                __${t}_debug "ActiveHelp will need delimiter"
                hasActiveHelp=1
            fi
            continue
        fi

        if [ -n "$comp" ]; then
            # If requested, completions are returned with a description.
            # The description is preceded by a TAB character.
            # For zsh's _describe, we need to use a : instead of a TAB.
            # We first need to escape any : as part of the completion itself.
            comp=\${comp//:/\\:}

            local tab="$(printf '\\t')"
            comp=\${comp//$tab/:}

            __${t}_debug "Adding completion: \${comp}"
            completions+=\${comp}
            lastComp=$comp
        fi
    done < <(printf "%s\n" "\${out[@]}")

    # Add a delimiter after the activeHelp statements, but only if:
    # - there are completions following the activeHelp statements, or
    # - file completion will be performed (so there will be choices after the activeHelp)
    if [ $hasActiveHelp -eq 1 ]; then
        if [ \${#completions} -ne 0 ] || [ $((directive & shellCompDirectiveNoFileComp)) -eq 0 ]; then
            __${t}_debug "Adding activeHelp delimiter"
            compadd -x "--"
            hasActiveHelp=0
        fi
    fi

    if [ $((directive & shellCompDirectiveNoSpace)) -ne 0 ]; then
        __${t}_debug "Activating nospace."
        noSpace="-S ''"
    fi

    if [ $((directive & shellCompDirectiveKeepOrder)) -ne 0 ]; then
        __${t}_debug "Activating keep order."
        keepOrder="-V"
    fi

    if [ $((directive & shellCompDirectiveFilterFileExt)) -ne 0 ]; then
        # File extension filtering
        local filteringCmd
        filteringCmd='_files'
        for filter in \${completions[@]}; do
            if [ \${filter[1]} != '*' ]; then
                # zsh requires a glob pattern to do file filtering
                filter="\\*.$filter"
            fi
            filteringCmd+=" -g $filter"
        done
        filteringCmd+=" \${flagPrefix}"

        __${t}_debug "File filtering command: $filteringCmd"
        _arguments '*:filename:'"$filteringCmd"
    elif [ $((directive & shellCompDirectiveFilterDirs)) -ne 0 ]; then
        # File completion for directories only
        local subdir
        subdir="\${completions[1]}"
        if [ -n "$subdir" ]; then
            __${t}_debug "Listing directories in $subdir"
            pushd "\${subdir}" >/dev/null 2>&1
        else
            __${t}_debug "Listing directories in ."
        fi

        local result
        _arguments '*:dirname:_files -/'" \${flagPrefix}"
        result=$?
        if [ -n "$subdir" ]; then
            popd >/dev/null 2>&1
        fi
        return $result
    else
        __${t}_debug "Calling _describe"
        if eval _describe $keepOrder "completions" completions -Q \${flagPrefix} \${noSpace}; then
            __${t}_debug "_describe found some completions"

            # Return the success of having called _describe
            return 0
        else
            __${t}_debug "_describe did not find completions."
            __${t}_debug "Checking if we should do file completion."
            if [ $((directive & shellCompDirectiveNoFileComp)) -ne 0 ]; then
                __${t}_debug "deactivating file completion"

                # Return 0 to indicate completion is finished and prevent zsh from
                # trying other completion algorithms (which could cause hanging).
                # We use NoFileComp directive to explicitly disable file completion.
                return 0
            else
                # Perform file completion
                __${t}_debug "Activating file completion"

                # We must return the result of this command, so it must be the
                # last command, or else we must store its result to return it.
                _arguments '*:filename:_files'" \${flagPrefix}"
            fi
        fi
    fi
}

# don't run the completion function when being sourced or eval-ed
if [ "\${funcstack[1]}" = "_${t}" ]; then
    _${t}
fi
`}function n(t,n){let r=t.replace(/[-:]/g,`_`);return`# bash completion for ${t}

# Define shell completion directives
readonly ShellCompDirectiveError=${e.ShellCompDirectiveError}
readonly ShellCompDirectiveNoSpace=${e.ShellCompDirectiveNoSpace}
readonly ShellCompDirectiveNoFileComp=${e.ShellCompDirectiveNoFileComp}
readonly ShellCompDirectiveFilterFileExt=${e.ShellCompDirectiveFilterFileExt}
readonly ShellCompDirectiveFilterDirs=${e.ShellCompDirectiveFilterDirs}
readonly ShellCompDirectiveKeepOrder=${e.ShellCompDirectiveKeepOrder}

# Function to debug completion
__${r}_debug() {
    if [[ -n \${BASH_COMP_DEBUG_FILE:-} ]]; then
        echo "$*" >> "\${BASH_COMP_DEBUG_FILE}"
    fi
}

# Function to handle completions
__${r}_complete() {
    local cur prev words cword
    _get_comp_words_by_ref -n "=:" cur prev words cword

    local requestComp out directive
    
    # Build the command to get completions
    requestComp="${n} complete -- \${words[@]:1}"
    
    # Add an empty parameter if the last parameter is complete
    if [[ -z "$cur" ]]; then
        requestComp="$requestComp ''"
    fi
    
    # Get completions from the program
    out=$(eval "$requestComp" 2>/dev/null)
    
    # Extract directive if present
    directive=0
    if [[ "$out" == *:* ]]; then
        directive=\${out##*:}
        out=\${out%:*}
    fi
    
    # Process completions based on directive
    if [[ $((directive & $ShellCompDirectiveError)) -ne 0 ]]; then
        # Error, no completion
        return
    fi
    
    # Apply directives
    if [[ $((directive & $ShellCompDirectiveNoSpace)) -ne 0 ]]; then
        compopt -o nospace
    fi
    if [[ $((directive & $ShellCompDirectiveKeepOrder)) -ne 0 ]]; then
        compopt -o nosort
    fi
    if [[ $((directive & $ShellCompDirectiveNoFileComp)) -ne 0 ]]; then
        compopt +o default
    fi
    
    # Handle file extension filtering
    if [[ $((directive & $ShellCompDirectiveFilterFileExt)) -ne 0 ]]; then
        local filter=""
        for ext in $out; do
            filter="$filter|$ext"
        done
        filter="\\.($filter)"
        compopt -o filenames
        COMPREPLY=( $(compgen -f -X "!$filter" -- "$cur") )
        return
    fi
    
    # Handle directory filtering
    if [[ $((directive & $ShellCompDirectiveFilterDirs)) -ne 0 ]]; then
        compopt -o dirnames
        COMPREPLY=( $(compgen -d -- "$cur") )
        return
    fi
    
    # Process completions
    local IFS=$'\\n'
    local tab=$(printf '\\t')
    
    # Parse completions with descriptions
    local completions=()
    while read -r comp; do
        if [[ "$comp" == *$tab* ]]; then
            # Split completion and description
            local value=\${comp%%$tab*}
            local desc=\${comp#*$tab}
            completions+=("$value")
        else
            completions+=("$comp")
        fi
    done <<< "$out"
    
    # Return completions
    COMPREPLY=( $(compgen -W "\${completions[*]}" -- "$cur") )
}

# Register completion function
complete -F __${r}_complete ${t}
`}function r(t,n){let r=t.replace(/[-:]/g,`_`),i=e.ShellCompDirectiveError,a=e.ShellCompDirectiveNoSpace,o=e.ShellCompDirectiveNoFileComp,s=e.ShellCompDirectiveFilterFileExt,c=e.ShellCompDirectiveFilterDirs;return`# fish completion for ${t} -*- shell-script -*-

function __${r}_debug
    set -l file "$BASH_COMP_DEBUG_FILE"
    if test -n "$file"
        echo "$argv" >> $file
    end
end

function __${r}_perform_completion
    __${r}_debug "Starting __${r}_perform_completion"

    # Extract all args except the last one
    set -l args (commandline -opc)
    # Extract the last arg and escape it in case it is a space or wildcard
    set -l lastArg (string escape -- (commandline -ct))

    __${r}_debug "args: $args"
    __${r}_debug "last arg: $lastArg"

    # Build the completion request command
    set -l requestComp "${n} complete -- (string join ' ' -- (string escape -- $args[2..-1])) $lastArg"

    __${r}_debug "Calling $requestComp"
    set -l results (eval $requestComp 2> /dev/null)

    # Some programs may output extra empty lines after the directive.
    # Let's ignore them or else it will break completion.
    # Ref: https://github.com/spf13/cobra/issues/1279
    for line in $results[-1..1]
        if test (string trim -- $line) = ""
            # Found an empty line, remove it
            set results $results[1..-2]
        else
            # Found non-empty line, we have our proper output
            break
        end
    end

    set -l comps $results[1..-2]
    set -l directiveLine $results[-1]

    # For Fish, when completing a flag with an = (e.g., <program> -n=<TAB>)
    # completions must be prefixed with the flag
    set -l flagPrefix (string match -r -- '-.*=' "$lastArg")

    __${r}_debug "Comps: $comps"
    __${r}_debug "DirectiveLine: $directiveLine"
    __${r}_debug "flagPrefix: $flagPrefix"

    for comp in $comps
        printf "%s%s\\n" "$flagPrefix" "$comp"
    end

    printf "%s\\n" "$directiveLine"
end

# This function limits calls to __${r}_perform_completion, by caching the result
function __${r}_perform_completion_once
    __${r}_debug "Starting __${r}_perform_completion_once"

    if test -n "$__${r}_perform_completion_once_result"
        __${r}_debug "Seems like a valid result already exists, skipping __${r}_perform_completion"
        return 0
    end

    set --global __${r}_perform_completion_once_result (__${r}_perform_completion)
    if test -z "$__${r}_perform_completion_once_result"
        __${r}_debug "No completions, probably due to a failure"
        return 1
    end

    __${r}_debug "Performed completions and set __${r}_perform_completion_once_result"
    return 0
end

# This function is used to clear the cached result after completions are run
function __${r}_clear_perform_completion_once_result
    __${r}_debug ""
    __${r}_debug "========= clearing previously set __${r}_perform_completion_once_result variable =========="
    set --erase __${r}_perform_completion_once_result
    __${r}_debug "Successfully erased the variable __${r}_perform_completion_once_result"
end

function __${r}_requires_order_preservation
    __${r}_debug ""
    __${r}_debug "========= checking if order preservation is required =========="

    __${r}_perform_completion_once
    if test -z "$__${r}_perform_completion_once_result"
        __${r}_debug "Error determining if order preservation is required"
        return 1
    end

    set -l directive (string sub --start 2 $__${r}_perform_completion_once_result[-1])
    __${r}_debug "Directive is: $directive"

    set -l shellCompDirectiveKeepOrder ${e.ShellCompDirectiveKeepOrder}
    set -l keeporder (math (math --scale 0 $directive / $shellCompDirectiveKeepOrder) % 2)
    __${r}_debug "Keeporder is: $keeporder"

    if test $keeporder -ne 0
        __${r}_debug "This does require order preservation"
        return 0
    end

    __${r}_debug "This doesn't require order preservation"
    return 1
end

# This function does two things:
# - Obtain the completions and store them in the global __${r}_comp_results
# - Return false if file completion should be performed
function __${r}_prepare_completions
    __${r}_debug ""
    __${r}_debug "========= starting completion logic =========="

    # Start fresh
    set --erase __${r}_comp_results

    __${r}_perform_completion_once
    __${r}_debug "Completion results: $__${r}_perform_completion_once_result"

    if test -z "$__${r}_perform_completion_once_result"
        __${r}_debug "No completion, probably due to a failure"
        # Might as well do file completion, in case it helps
        return 1
    end

    set -l directive (string sub --start 2 $__${r}_perform_completion_once_result[-1])
    set --global __${r}_comp_results $__${r}_perform_completion_once_result[1..-2]

    __${r}_debug "Completions are: $__${r}_comp_results"
    __${r}_debug "Directive is: $directive"

    set -l shellCompDirectiveError ${i}
    set -l shellCompDirectiveNoSpace ${a}
    set -l shellCompDirectiveNoFileComp ${o}
    set -l shellCompDirectiveFilterFileExt ${s}
    set -l shellCompDirectiveFilterDirs ${c}

    if test -z "$directive"
        set directive 0
    end

    set -l compErr (math (math --scale 0 $directive / $shellCompDirectiveError) % 2)
    if test $compErr -eq 1
        __${r}_debug "Received error directive: aborting."
        # Might as well do file completion, in case it helps
        return 1
    end

    set -l filefilter (math (math --scale 0 $directive / $shellCompDirectiveFilterFileExt) % 2)
    set -l dirfilter (math (math --scale 0 $directive / $shellCompDirectiveFilterDirs) % 2)
    if test $filefilter -eq 1; or test $dirfilter -eq 1
        __${r}_debug "File extension filtering or directory filtering not supported"
        # Do full file completion instead
        return 1
    end

    set -l nospace (math (math --scale 0 $directive / $shellCompDirectiveNoSpace) % 2)
    set -l nofiles (math (math --scale 0 $directive / $shellCompDirectiveNoFileComp) % 2)

    __${r}_debug "nospace: $nospace, nofiles: $nofiles"

    # If we want to prevent a space, or if file completion is NOT disabled,
    # we need to count the number of valid completions.
    # To do so, we will filter on prefix as the completions we have received
    # may not already be filtered so as to allow fish to match on different
    # criteria than the prefix.
    if test $nospace -ne 0; or test $nofiles -eq 0
        set -l prefix (commandline -t | string escape --style=regex)
        __${r}_debug "prefix: $prefix"

        set -l completions (string match -r -- "^$prefix.*" $__${r}_comp_results)
        set --global __${r}_comp_results $completions
        __${r}_debug "Filtered completions are: $__${r}_comp_results"

        # Important not to quote the variable for count to work
        set -l numComps (count $__${r}_comp_results)
        __${r}_debug "numComps: $numComps"

        if test $numComps -eq 1; and test $nospace -ne 0
            # We must first split on \\t to get rid of the descriptions to be
            # able to check what the actual completion will be.
            # We don't need descriptions anyway since there is only a single
            # real completion which the shell will expand immediately.
            set -l split (string split --max 1 "\\t" $__${r}_comp_results[1])

            # Fish won't add a space if the completion ends with any
            # of the following characters: @=/:.,
            set -l lastChar (string sub -s -1 -- $split)
            if not string match -r -q "[@=/:.,]" -- "$lastChar"
                # In other cases, to support the "nospace" directive we trick the shell
                # by outputting an extra, longer completion.
                __${r}_debug "Adding second completion to perform nospace directive"
                set --global __${r}_comp_results $split[1] $split[1].
                __${r}_debug "Completions are now: $__${r}_comp_results"
            end
        end

        if test $numComps -eq 0; and test $nofiles -eq 0
            # To be consistent with bash and zsh, we only trigger file
            # completion when there are no other completions
            __${r}_debug "Requesting file completion"
            return 1
        end
    end

    return 0
end

# Since Fish completions are only loaded once the user triggers them, we trigger them ourselves
# so we can properly delete any completions provided by another script.
# Only do this if the program can be found, or else fish may print some errors; besides,
# the existing completions will only be loaded if the program can be found.
if type -q "${t}"
    # The space after the program name is essential to trigger completion for the program
    # and not completion of the program name itself.
    # Also, we use '> /dev/null 2>&1' since '&>' is not supported in older versions of fish.
    complete --do-complete "${t} " > /dev/null 2>&1
end

# Remove any pre-existing completions for the program since we will be handling all of them.
complete -c ${t} -e

# This will get called after the two calls below and clear the cached result
complete -c ${t} -n '__${r}_clear_perform_completion_once_result'
# The call to __${r}_prepare_completions will setup __${r}_comp_results
# which provides the program's completion choices.
# If this doesn't require order preservation, we don't use the -k flag
complete -c ${t} -n 'not __${r}_requires_order_preservation && __${r}_prepare_completions' -f -a '$__${r}_comp_results'
# Otherwise we use the -k flag
complete -k -c ${t} -n '__${r}_requires_order_preservation && __${r}_prepare_completions' -f -a '$__${r}_comp_results'
`}function i(t,n){let r=t.replace(/[-:]/g,`_`);return`# powershell completion for ${t} -*- shell-script -*-

  [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    function __${t}_debug {
        if ($env:BASH_COMP_DEBUG_FILE) {
            "$args" | Out-File -Append -FilePath "$env:BASH_COMP_DEBUG_FILE"
        }
    }

    filter __${t}_escapeStringWithSpecialChars {
        $_ -replace '\\s|#|@|\\$|;|,|''|\\{|\\}|\\(|\\)|"|\\||<|>|&','\`$&'
    }

[scriptblock]$__${r}CompleterBlock = {
    param(
            $WordToComplete,
            $CommandAst,
            $CursorPosition
        )

    # Get the current command line and convert into a string
    $Command = $CommandAst.CommandElements
    $Command = "$Command"

    __${t}_debug ""
    __${t}_debug "========= starting completion logic =========="
    __${t}_debug "WordToComplete: $WordToComplete Command: $Command CursorPosition: $CursorPosition"

    # The user could have moved the cursor backwards on the command-line.
    # We need to trigger completion from the $CursorPosition location, so we need
    # to truncate the command-line ($Command) up to the $CursorPosition location.
    # Make sure the $Command is longer then the $CursorPosition before we truncate.
    # This happens because the $Command does not include the last space.
    if ($Command.Length -gt $CursorPosition) {
        $Command = $Command.Substring(0, $CursorPosition)
    }
    __${t}_debug "Truncated command: $Command"

    $ShellCompDirectiveError=${e.ShellCompDirectiveError}
    $ShellCompDirectiveNoSpace=${e.ShellCompDirectiveNoSpace}
    $ShellCompDirectiveNoFileComp=${e.ShellCompDirectiveNoFileComp}
    $ShellCompDirectiveFilterFileExt=${e.ShellCompDirectiveFilterFileExt}
    $ShellCompDirectiveFilterDirs=${e.ShellCompDirectiveFilterDirs}
    $ShellCompDirectiveKeepOrder=${e.ShellCompDirectiveKeepOrder}

    # Prepare the command to request completions for the program.
    # Split the command at the first space to separate the program and arguments.
    $Program, $Arguments = $Command.Split(" ", 2)

    $QuotedArgs = ($Arguments -split ' ' | ForEach-Object { "'" + ($_ -replace "'", "''") + "'" }) -join ' '
    __${t}_debug "QuotedArgs: $QuotedArgs"

    $RequestComp = "& ${n} complete '--' $QuotedArgs"
    __${t}_debug "RequestComp: $RequestComp"

    # we cannot use $WordToComplete because it
    # has the wrong values if the cursor was moved
    # so use the last argument
    if ($WordToComplete -ne "" ) {
        $WordToComplete = $Arguments.Split(" ")[-1]
    }
    __${t}_debug "New WordToComplete: $WordToComplete"


    # Check for flag with equal sign
    $IsEqualFlag = ($WordToComplete -Like "--*=*" )
    if ( $IsEqualFlag ) {
        __${t}_debug "Completing equal sign flag"
        # Remove the flag part
        $Flag, $WordToComplete = $WordToComplete.Split("=", 2)
    }

    if ( $WordToComplete -eq "" -And ( -Not $IsEqualFlag )) {
        # If the last parameter is complete (there is a space following it)
        # We add an extra empty parameter so we can indicate this to the go method.
        __${t}_debug "Adding extra empty parameter"
        # PowerShell 7.2+ changed the way how the arguments are passed to executables,
        # so for pre-7.2 or when Legacy argument passing is enabled we need to use
        if ($PSVersionTable.PsVersion -lt [version]'7.2.0' -or
            ($PSVersionTable.PsVersion -lt [version]'7.3.0' -and -not [ExperimentalFeature]::IsEnabled("PSNativeCommandArgumentPassing")) -or
            (($PSVersionTable.PsVersion -ge [version]'7.3.0' -or [ExperimentalFeature]::IsEnabled("PSNativeCommandArgumentPassing")) -and
              $PSNativeCommandArgumentPassing -eq 'Legacy')) {
             $RequestComp="$RequestComp" + ' \`"\`"'
        } else {
             $RequestComp = "$RequestComp" + ' ""'
        }
    }

    __${t}_debug "Calling $RequestComp"
    # First disable ActiveHelp which is not supported for Powershell
    $env:ActiveHelp = 0

    # call the command store the output in $out and redirect stderr and stdout to null
    # $Out is an array contains each line per element
    Invoke-Expression -OutVariable out "$RequestComp" 2>&1 | Out-Null

    # get directive from last line
    [int]$Directive = $Out[-1].TrimStart(':')
    if ($Directive -eq "") {
        # There is no directive specified
        $Directive = 0
    }
    __${t}_debug "The completion directive is: $Directive"

    # remove directive (last element) from out
    $Out = $Out | Where-Object { $_ -ne $Out[-1] }
    __${t}_debug "The completions are: $Out"

    if (($Directive -band $ShellCompDirectiveError) -ne 0 ) {
        # Error code.  No completion.
        __${t}_debug "Received error from custom completion go code"
        return
    }

    $Longest = 0
    [Array]$Values = $Out | ForEach-Object {
        # Split the output in name and description
        $Name, $Description = $_.Split("\`t", 2)
        __${t}_debug "Name: $Name Description: $Description"

        # Look for the longest completion so that we can format things nicely
        if ($Longest -lt $Name.Length) {
            $Longest = $Name.Length
        }

        # Set the description to a one space string if there is none set.
        # This is needed because the CompletionResult does not accept an empty string as argument
        if (-Not $Description) {
            $Description = " "
        }
        @{ Name = "$Name"; Description = "$Description" }
    }


    $Space = " "
    if (($Directive -band $ShellCompDirectiveNoSpace) -ne 0 ) {
        # remove the space here
        __${t}_debug "ShellCompDirectiveNoSpace is called"
        $Space = ""
    }

    if ((($Directive -band $ShellCompDirectiveFilterFileExt) -ne 0 ) -or
       (($Directive -band $ShellCompDirectiveFilterDirs) -ne 0 ))  {
        __${t}_debug "ShellCompDirectiveFilterFileExt ShellCompDirectiveFilterDirs are not supported"

        # return here to prevent the completion of the extensions
        return
    }

    $Values = $Values | Where-Object {
        # filter the result
        $_.Name -like "$WordToComplete*"

        # Join the flag back if we have an equal sign flag
        if ( $IsEqualFlag ) {
            __${t}_debug "Join the equal sign flag back to the completion value"
            $_.Name = $Flag + "=" + $_.Name
        }
    }

    # we sort the values in ascending order by name if keep order isn't passed
    if (($Directive -band $ShellCompDirectiveKeepOrder) -eq 0 ) {
        $Values = $Values | Sort-Object -Property Name
    }

    if (($Directive -band $ShellCompDirectiveNoFileComp) -ne 0 ) {
        __${t}_debug "ShellCompDirectiveNoFileComp is called"

        if ($Values.Length -eq 0) {
            # Just print an empty string here so the
            # shell does not start to complete paths.
            # We cannot use CompletionResult here because
            # it does not accept an empty string as argument.
            ""
            return
        }
    }

    # Get the current mode
    $Mode = (Get-PSReadLineKeyHandler | Where-Object { $_.Key -eq "Tab" }).Function
    __${t}_debug "Mode: $Mode"

    $Values | ForEach-Object {

        # store temporary because switch will overwrite $_
        $comp = $_

        # PowerShell supports three different completion modes
        # - TabCompleteNext (default windows style - on each key press the next option is displayed)
        # - Complete (works like bash)
        # - MenuComplete (works like zsh)
        # You set the mode with Set-PSReadLineKeyHandler -Key Tab -Function <mode>

        # CompletionResult Arguments:
        # 1) CompletionText text to be used as the auto completion result
        # 2) ListItemText   text to be displayed in the suggestion list
        # 3) ResultType     type of completion result
        # 4) ToolTip        text for the tooltip with details about the object

        switch ($Mode) {

            # bash like
            "Complete" {

                if ($Values.Length -eq 1) {
                    __${t}_debug "Only one completion left"

                    # insert space after value
                    [System.Management.Automation.CompletionResult]::new($($comp.Name | __${t}_escapeStringWithSpecialChars) + $Space, "$($comp.Name)", 'ParameterValue', "$($comp.Description)")

                } else {
                    # Add the proper number of spaces to align the descriptions
                    while($comp.Name.Length -lt $Longest) {
                        $comp.Name = $comp.Name + " "
                    }

                    # Check for empty description and only add parentheses if needed
                    if ($($comp.Description) -eq " " ) {
                        $Description = ""
                    } else {
                        $Description = "  ($($comp.Description))"
                    }

                    [System.Management.Automation.CompletionResult]::new("$($comp.Name)$Description", "$($comp.Name)$Description", 'ParameterValue', "$($comp.Description)")
                }
             }

            # zsh like
            "MenuComplete" {
                # insert space after value
                # MenuComplete will automatically show the ToolTip of
                # the highlighted value at the bottom of the suggestions.
                [System.Management.Automation.CompletionResult]::new($($comp.Name | __${t}_escapeStringWithSpecialChars) + $Space, "$($comp.Name)", 'ParameterValue', "$($comp.Description)")
            }

            # TabCompleteNext and in case we get something unknown
            Default {
                # Like MenuComplete but we don't want to add a space here because
                # the user need to press space anyway to get the completion.
                # Description will not be shown because that's not possible with TabCompleteNext
                [System.Management.Automation.CompletionResult]::new($($comp.Name | __${t}_escapeStringWithSpecialChars), "$($comp.Name)", 'ParameterValue', "$($comp.Description)")
            }
        }

    }
}

Register-ArgumentCompleter -CommandName '${t}' -ScriptBlock $__${r}CompleterBlock
`}export{t as i,r as n,n as r,i as t};