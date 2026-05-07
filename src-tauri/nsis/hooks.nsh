!macro NSIS_HOOK_PREINSTALL
  !insertmacro CheckIfAppIsRunning "${MAINBINARYNAME}.exe" "${PRODUCTNAME}"

  ReadRegStr $R9 SHCTX "${MANUPRODUCTKEY}" ""
  StrCmp "$R9" "" mtga_check_files 0
  StrCmp "$R9" "$INSTDIR" mtga_check_runtime 0

mtga_check_files:
  IfFileExists "$INSTDIR\mtga-tauri.exe" mtga_check_runtime 0
  IfFileExists "$INSTDIR\Lib\site-packages\mtga_app\__init__.py" mtga_check_modules 0
  Goto mtga_cleanup_done

mtga_check_modules:
  IfFileExists "$INSTDIR\Lib\site-packages\modules\__init__.py" mtga_check_runtime 0
  Goto mtga_cleanup_done

mtga_check_runtime:
  IfFileExists "$INSTDIR\python313.dll" mtga_cleanup_runtime 0
  IfFileExists "$INSTDIR\python313.zip" mtga_cleanup_runtime 0
  IfFileExists "$INSTDIR\Lib\site-packages\mtga_app" mtga_cleanup_runtime 0
  IfFileExists "$INSTDIR\Lib\site-packages\modules" mtga_cleanup_runtime 0
  IfFileExists "$INSTDIR\Lib\site-packages\sniffio" mtga_cleanup_runtime 0
  IfFileExists "$INSTDIR\Lib\site-packages\*.dist-info" mtga_cleanup_runtime 0
  Goto mtga_cleanup_done

mtga_cleanup_runtime:
  DetailPrint "Cleaning previous embedded runtime from $INSTDIR"
  RMDir /r "$INSTDIR\DLLs"
  RMDir /r "$INSTDIR\include"
  RMDir /r "$INSTDIR\Lib"
  RMDir /r "$INSTDIR\libs"
  Delete "$INSTDIR\python.exe"
  Delete "$INSTDIR\pythonw.exe"
  Delete "$INSTDIR\python3.dll"
  Delete "$INSTDIR\python313.dll"
  Delete "$INSTDIR\python313.zip"
  Delete "$INSTDIR\vcruntime140.dll"
  Delete "$INSTDIR\vcruntime140_1.dll"

mtga_cleanup_done:
!macroend
