; Inno Setup script for Ticket Manager (requires Inno Setup 6.3 or newer).
; Build with build_windows.bat, or open this file in the Inno Setup
; Compiler and press Compile (after running PyInstaller so that
; dist\TicketManager.exe exists).

#define MyAppName "Ticket Manager"
#define MyAppVersion "1.0"
#define MyAppPublisher "Karcha Studios"
#define MyAppURL "https://karcha3.github.io/ticketmanager"
#define MyAppExeName "TicketManager.exe"

[Setup]
; Unique ID for this app. Never change it, or updates will install side by side.
AppId={{ECDA3D4E-EB36-4637-8B13-769EB6B2D056}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
; The user must accept the license before installing.
LicenseFile=..\LICENSE.txt
OutputDir=..\installer_output
OutputBaseFilename=TicketManager-Setup-{#MyAppVersion}
SetupIconFile=..\assets\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
; Installs just for the current user by default (no admin prompt);
; the dialog lets the user choose "for all users" instead.
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

; Note: tickets are stored in %APPDATA%\TicketManager, outside the install
; folder, so uninstalling or upgrading never deletes the user's data.
