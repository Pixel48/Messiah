; === Messiah-setup.nsi ===
; Includes
  ; Modern UI 2
  !include "MUI2.nsh"
    ; Icons
    !define MUI_ICON "./icons/ico.ico"
    !define MUI_UNICON "./icons/unico.ico"
    ; Directory page
    !define MUI_DIRECTORYPAGE_TEXT_TOP "Thanks for choosing Messiah!"
    ; Uninstall Directory page
    !define MUI_UNCONFIRMPAGE_TEXT_TOP "Uninstall Messiah?"

; Defines
!define PROG_NAME "Messiah"
!define VERSION "0.3.1"
!define PUBLISHER "GitHub.com/Pixel48"
!define INST_KEY "SOFTWARE\${PROG_NAME}"
!define UNINST_KEY "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${PROG_NAME}"
!define DESKTOP_SHORTCUT "$DESKTOP\${PROG_NAME}.lnk"

; Settings
Name "${PROG_NAME}"
OutFile "pyinst\Setup_${PROG_NAME}.exe"
RequestExecutionLevel admin
InstallDir "$PROGRAMFILES64\${PROG_NAME}"
!define UNINSTDIR "$INSTDIR\Uninstall ${PROG_NAME}.exe"

; Pages
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

; Installer
Section "${PROG_NAME}" install
  SetOutPath $INSTDIR
  File /r "pyinst\dist\${PROG_NAME}\*"
  ; Registry setup
    ; Instalation info
    WriteRegStr HKLM "${INST_KEY}" "InstallDir" "$INSTDIR"
    WriteRegStr HKLM "${INST_KEY}" "DisplayName" "${PROG_NAME}"
    WriteRegStr HKLM "${INST_KEY}" "DisplayVersion" "${VERSION}"
    WriteRegStr HKLM "${INST_KEY}" "Publisher" "${PUBLISHER}"
    WriteRegStr HKLM "${INST_KEY}" "UninstallString" "${UNINSTDIR}"
    ; Uninstaller
    WriteUninstaller "${UNINSTDIR}"
    WriteRegStr HKLM "${UNINST_KEY}" "InstallDir" "$INSTDIR"
    WriteRegStr HKLM "${UNINST_KEY}" "DisplayName" "${PROG_NAME}"
    WriteRegStr HKLM "${UNINST_KEY}" "DisplayVersion" "${VERSION}"
    WriteRegStr HKLM "${UNINST_KEY}" "DisplayIcon" "$INSTDIR\${PROG_NAME}.exe"
    WriteRegStr HKLM "${UNINST_KEY}" "Publisher" "${PUBLISHER}"
    WriteRegStr HKLM "${UNINST_KEY}" "UninstallString" "${UNINSTDIR}"
    WriteRegDWORD HKLM "${UNINST_KEY}" "NoModify" 1
    WriteRegDWORD HKLM "${UNINST_KEY}" "NoRepair" 1
SectionEnd

Section "Desktop Shortcut" Desktop_lnk
  CreateShortCut "${DESKTOP_SHORTCUT}" "$INSTDIR\${PROG_NAME}"
SectionEnd

; Uninstaller
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

Section "Uninstall" uninstall
  Delete "${DESKTOP_SHORTCUT}"
  Delete "${UNINSTDIR}"
  RMDir /r "$INSTDIR"
  DeleteRegKey HKLM "${INST_KEY}"
  DeleteRegKey HKLM "${UNINST_KEY}"
SectionEnd
