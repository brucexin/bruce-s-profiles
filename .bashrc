# .bashrc - Joshua Uziel - Feel free to use any part of this.

# The almighty $PATH
PATH="$HOME/bin:/usr/local/bin:/bin:/usr/bin:/sbin:/usr/sbin:/usr/games:/usr/X11R6/bin"

export PATH

umask 022

#LANG=en_US.ISO8859-1
#LC_ALL=en_US.ISO8859-1

# Aliases
alias ls='ls --color=auto -CF'
alias rm='rm -i'
alias cp='cp -i'
alias grep="grep --color=auto"
LC_ALL=zh_CN.UTF8

echo -ne '\e%G\e[?47h\e%G\e[?47l'





##################################################
# Fancy PWD display function
##################################################
# The home directory (HOME) is replaced with a ~
# The last pwdmaxlen characters of the PWD are displayed
# Leading partial directory names are striped off
# /home/me/stuff          -> ~/stuff               if USER=me
# /usr/share/big_dir_name -> ../share/big_dir_name if pwdmaxlen=20
##################################################
bash_prompt_command() {
	    # How many characters of the $PWD should be kept
	        local pwdmaxlen=25
		    # Indicate that there has been dir truncation
		        local trunc_symbol=".."
			    local dir=${PWD##*/}
			        pwdmaxlen=$(( ( pwdmaxlen < ${#dir} ) ? ${#dir} : pwdmaxlen ))
				    NEW_PWD=${PWD/#$HOME/\~}
				        local pwdoffset=$(( ${#NEW_PWD} - pwdmaxlen ))
					    if [ ${pwdoffset} -gt "0" ]
						        then
								        NEW_PWD=${NEW_PWD:$pwdoffset:$pwdmaxlen}
									        NEW_PWD=${trunc_symbol}/${NEW_PWD#*/}
										    fi
									    }

bash_prompt() {
	    case $TERM in
		         xterm*|rxvt*)
			          local TITLEBAR='\[\033]0;\u:${NEW_PWD}\007\]'
				            ;;
					         *)
						          local TITLEBAR=""
							            ;;
								        esac
									    local NONE="\[\033[0m\]"    # unsets color to term's fg color
									        
									        # regular colors
										    local K="\[\033[0;30m\]"    # black
										        local R="\[\033[0;31m\]"    # red
											    local G="\[\033[0;32m\]"    # green
											        local Y="\[\033[0;33m\]"    # yellow
												    local B="\[\033[0;34m\]"    # blue
												        local M="\[\033[0;35m\]"    # magenta
													    local C="\[\033[0;36m\]"    # cyan
													        local W="\[\033[0;37m\]"    # white
														    
														    # emphasized (bolded) colors
														        local EMK="\[\033[1;30m\]"
															    local EMR="\[\033[1;31m\]"
															        local EMG="\[\033[1;32m\]"
																    local EMY="\[\033[1;33m\]"
																        local EMB="\[\033[1;34m\]"
																	    local EMM="\[\033[1;35m\]"
																	        local EMC="\[\033[1;36m\]"
																		    local EMW="\[\033[1;37m\]"
																		        
																		        # background colors
																			    local BGK="\[\033[40m\]"
																			        local BGR="\[\033[41m\]"
																				    local BGG="\[\033[42m\]"
																				        local BGY="\[\033[43m\]"
																					    local BGB="\[\033[44m\]"
																					        local BGM="\[\033[45m\]"
																						    local BGC="\[\033[46m\]"
																						        local BGW="\[\033[47m\]"
																							    
																							    local UC=$W                 # user's color
																							        [ $UID -eq "0" ] && UC=$R   # root's color
																								    
																								    PS1="$TITLEBAR ${EMK}[${UC}\u${EMK}@${UC}\h ${EMB}\${NEW_PWD}${EMK}]${UC}\\$ ${NONE}"
																								        # without colors: PS1="[\u@\h \${NEW_PWD}]\\$ "
																									    # extra backslash in front of \$ to make bash colorize the prompt
																								    }

																				PROMPT_COMMAND=bash_prompt_command
																				bash_prompt
																				unset bash_prompt

