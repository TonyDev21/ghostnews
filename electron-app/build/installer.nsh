; Custom NSIS installer script for GHOST NEWS
!macro customInstall
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${UNINSTALL_APP_KEY}" "DisplayName" "GHOST NEWS - Analizador de Noticias"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${UNINSTALL_APP_KEY}" "Publisher" "TonyDev21"
!macroend
