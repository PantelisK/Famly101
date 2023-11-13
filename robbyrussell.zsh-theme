setopt prompt_subst
function getCluster() {
  export CLUSTER=$(kubectl config current-context)
  PROMPT="%F{208}% [pant] %F{155}[%w]%F{111} [${CLUSTER}] %(?:%{$fg_bold[green]%}➜ :%{$fg_bold[red]%}➜ ) %{$fg[cyan]%}%3c%{$reset_color%}"
  PROMPT+=' $(git_prompt_info)'
}
typeset -a precmd_functions
precmd_functions=(getCluster)

ZSH_THEME_GIT_PROMPT_PREFIX="%{$fg_bold[blue]%}git:(%{$fg[red]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%} "
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[blue]%}) %{$fg[yellow]%}✗"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[blue]%})"
