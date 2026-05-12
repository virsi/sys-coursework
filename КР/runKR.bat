@echo off
rem ===========================================================
rem  runKR.bat - сборка и запуск курсовой работы
rem  Воробьев Е. А., ИУ5-42Б, вариант №5, 2026 г.
rem
rem  Запуск под DOSBox / MS DOS:
rem    runKR             - полный цикл: компиляция + линковка + запуск
rem    runKR build       - только сборка tsr.com
rem    runKR run         - только запуск tsr.com (без пересборки)
rem    runKR mem         - показать карту памяти (mem /P)
rem    runKR unload      - выгрузить резидент (повторный запуск tsr.com)
rem    runKR clean       - удалить артефакты сборки
rem    runKR help        - эта справка
rem ===========================================================

if "%1"==""        goto FULL
if "%1"=="build"   goto BUILD
if "%1"=="run"     goto RUN
if "%1"=="mem"     goto MEM
if "%1"=="unload"  goto UNLOAD
if "%1"=="clean"   goto CLEAN
if "%1"=="help"    goto HELP
if "%1"=="/?"      goto HELP

echo Неизвестная команда: %1
echo Используй: runKR help
goto END

rem -----------------------------------------------------------
:FULL
echo === [1/3] Компиляция tsr.asm ===
tasm.exe /l tsr.asm
if errorlevel 1 goto FAIL_TASM

echo.
echo === [2/3] Линковка tsr.obj в tsr.com ===
tlink.exe /t /x tsr.obj
if errorlevel 1 goto FAIL_TLINK

echo.
echo === [3/3] Запуск tsr.com ===
echo (резидент будет загружен в память; для выгрузки запусти tsr.com повторно)
tsr.com
goto END

rem -----------------------------------------------------------
:BUILD
echo === Компиляция tsr.asm ===
tasm.exe /l tsr.asm
if errorlevel 1 goto FAIL_TASM

echo.
echo === Линковка tsr.obj в tsr.com ===
tlink.exe /t /x tsr.obj
if errorlevel 1 goto FAIL_TLINK

echo.
echo === Сборка завершена ===
dir tsr.com
goto END

rem -----------------------------------------------------------
:RUN
if not exist tsr.com goto NO_COM
echo === Запуск tsr.com ===
tsr.com
goto END

rem -----------------------------------------------------------
:MEM
echo === Карта памяти ===
mem.exe /P
goto END

rem -----------------------------------------------------------
:UNLOAD
if not exist tsr.com goto NO_COM
echo === Выгрузка резидента (повторный запуск без параметров) ===
tsr.com
goto END

rem -----------------------------------------------------------
:CLEAN
echo === Удаление артефактов сборки ===
if exist tsr.obj del tsr.obj
if exist tsr.lst del tsr.lst
if exist tsr.map del tsr.map
if exist tsr.com del tsr.com
echo Удалены: tsr.obj, tsr.lst, tsr.map, tsr.com
goto END

rem -----------------------------------------------------------
:HELP
echo runKR.bat - сборка и запуск курсовой работы
echo Воробьев Е. А., ИУ5-42Б, вариант №5
echo.
echo Использование:
echo   runKR             - полный цикл (сборка + запуск)
echo   runKR build       - только сборка tsr.com
echo   runKR run         - только запуск tsr.com
echo   runKR mem         - показать карту памяти
echo   runKR unload      - выгрузить резидент
echo   runKR clean       - удалить артефакты сборки
echo   runKR help        - эта справка
echo.
echo Зависимости в PATH:
echo   tasm.exe   - Turbo Assembler 3.1+
echo   tlink.exe  - Turbo Link 5.1+
echo   mem.exe    - утилита диагностики памяти DOS
echo.
echo Функции программы (вариант 5):
echo   F8 - вывод подписи через 5 сек в верх экрана
echo   F9 - курсивное начертание буквы 'З'
echo   F1 - русификация клавиш T, ;, P, B, R - ЕЖЗИК
echo   F2 - ограничение ввода русских букв
echo   tsr /? - справка
echo   tsr    - повторно: выгрузка
goto END

rem -----------------------------------------------------------
:FAIL_TASM
echo.
echo ОШИБКА: компиляция tasm.exe завершилась неудачно.
echo Проверь синтаксис tsr.asm и наличие tasm.exe в PATH.
goto END

:FAIL_TLINK
echo.
echo ОШИБКА: линковка tlink.exe завершилась неудачно.
echo Проверь tsr.obj и наличие tlink.exe в PATH.
goto END

:NO_COM
echo.
echo ОШИБКА: файл tsr.com не найден.
echo Сначала собери проект: runKR build
goto END

rem -----------------------------------------------------------
:END
