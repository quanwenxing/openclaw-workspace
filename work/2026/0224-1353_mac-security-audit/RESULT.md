## Listening ports
COMMAND     PID     USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Postman     633 username   83u  IPv6 0x85c44fcdeceddea3      0t0  TCP *:15611 (LISTEN)
Discord    1055 username   40u  IPv4 0xb0d73d7b82c97679      0t0  TCP 127.0.0.1:6463 (LISTEN)
node      15030 username   16u  IPv4   0x4e84ac22b729f3      0t0  TCP 127.0.0.1:18789 (LISTEN)
node      15030 username   17u  IPv6 0x433cf304924fdd77      0t0  TCP [::1]:18789 (LISTEN)
node      15030 username   19u  IPv4 0x2d31c5afbc88b085      0t0  TCP 127.0.0.1:18792 (LISTEN)
java      15054 username   55u  IPv6 0x617b289afc6ce5a3      0t0  TCP 127.0.0.1:8080 (LISTEN)

## Remote login/screen sharing
You need administrator access to run this tool... exiting!
		"com.apple.screensharing" => disabled
		"com.openssh.sshd" => disabled

## Login history
username   ttys001                         Tue Feb 24 08:40 - 08:40  (00:00)
username   ttys001                         Tue Feb 24 08:35 - 08:35  (00:00)
username   ttys000                         Tue Feb 24 08:32 - 08:32  (00:00)
username   tty??    100.120.10.60          Mon Feb 23 14:42 - 14:42  (00:00)
username   tty??    100.120.10.60          Mon Feb 23 14:42 - 14:42  (00:00)
username   tty??    100.120.10.60          Mon Feb 23 14:42 - 14:42  (00:00)
username   ttys000                         Mon Feb 23 13:17 - 13:17  (00:00)
username   ttys000                         Mon Feb 23 13:08 - 13:08  (00:00)
username   ttys000                         Mon Feb 23 12:53 - 12:53  (00:00)
username   tty??    100.120.10.60          Mon Feb 23 12:48 - 12:48  (00:00)
username   tty??    100.120.10.60          Mon Feb 23 12:48 - 12:48  (00:00)
username   tty??    100.120.10.60          Mon Feb 23 12:48 - 12:48  (00:00)
username   tty??    100.120.10.60          Mon Feb 23 12:48 - 12:48  (00:00)
username   tty??    100.120.10.60          Mon Feb 23 12:48 - 12:48  (00:00)
username   tty??    100.120.10.60          Mon Feb 23 12:48 - 12:48  (00:00)
username   tty??    100.120.10.60          Mon Feb 23 12:47 - 12:47  (00:00)
username   tty??    100.120.10.60          Mon Feb 23 12:47 - 12:47  (00:00)
username   tty??    100.120.10.60          Mon Feb 23 12:47 - 12:47  (00:00)
username   tty??    100.120.10.60          Mon Feb 23 12:47 - 12:47  (00:00)
username   tty??    100.120.10.60          Mon Feb 23 12:47 - 12:47  (00:00)

## Persistence: LaunchAgents/Daemons
total 24
drwxr-xr-x   5 root  wheel   160 Feb 20 07:25 .
drwxr-xr-x  67 root  wheel  2144 Feb 18 22:46 ..
-rw-r--r--   1 root  wheel   181 Feb 18 22:47 com.google.keystone.agent.plist
-rw-r--r--   1 root  wheel   181 Feb 18 22:47 com.google.keystone.xpcservice.plist
-rw-r--r--   1 root  wheel   626 Jan  1  2001 org.chromium.chromoting.plist
total 32
drwxr-xr-x   6 root  wheel   192 Feb 23 12:32 .
drwxr-xr-x  67 root  wheel  2144 Feb 18 22:46 ..
-rw-r--r--   1 root  wheel   897 Feb 18 22:46 com.google.GoogleUpdater.wake.system.plist
-rw-r--r--   1 root  wheel   181 Feb 18 22:47 com.google.keystone.daemon.plist
-rw-r--r--@  1 root  admin   783 Feb 23 12:32 homebrew.mxcl.tailscale.plist
-rw-r--r--   1 root  wheel   578 Jan  1  2001 org.chromium.chromoting.broker.plist
total 32
drwx------@  6 username  staff   192 Feb  2 22:26 .
drwx------@ 84 username  staff  2688 Feb 16 10:20 ..
-rw-r--r--@  1 username  staff  2101 Feb 24 08:41 ai.openclaw.gateway.plist
-rw-r--r--@  1 username  staff   875 Feb  2 21:58 com.google.GoogleUpdater.wake.plist
-rw-r--r--@  1 username  staff   181 Feb  2 21:58 com.google.keystone.agent.plist
-rw-r--r--@  1 username  staff   181 Feb  2 21:58 com.google.keystone.xpcservice.plist

## Cron/at
crontab: no crontab for username
sudo: a password is required

## OpenClaw security audit deep
OpenClaw security audit
Summary: 0 critical · 1 warn · 1 info
Run deeper: openclaw security audit --deep

WARN
gateway.trusted_proxies_missing Reverse proxy headers are not trusted
  gateway.bind is loopback and gateway.trustedProxies is empty. If you expose the Control UI through a reverse proxy, configure trusted proxies so local-client checks cannot be spoofed.
  Fix: Set gateway.trustedProxies to your proxy IPs or keep the Control UI local-only.

INFO
summary.attack_surface Attack surface summary
  groups: open=0, allowlist=1
tools.elevated: enabled
hooks.webhooks: disabled
hooks.internal: enabled
browser control: enabled

## OpenClaw status
OpenClaw status

Overview
┌─────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Item            │ Value                                                                                             │
├─────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Dashboard       │ http://127.0.0.1:18789/                                                                           │
│ OS              │ macos 26.3 (arm64) · node 22.22.0                                                                 │
│ Tailscale       │ off                                                                                               │
│ Channel         │ stable (default)                                                                                  │
│ Update          │ pnpm · npm latest 2026.2.22-2                                                                     │
│ Gateway         │ local · ws://127.0.0.1:18789 (local loopback) · reachable 32ms · auth token · usernamenoMac-mini. │
│                 │ local (192.168.0.243) app 2026.2.22-2 macos 26.3                                                  │
│ Gateway service │ LaunchAgent installed · loaded · running (pid 15028, state active)                                │
│ Node service    │ LaunchAgent not installed                                                                         │
│ Agents          │ 1 · no bootstraps · sessions 19 · default main active 1m ago                                      │
│ Memory          │ 0 files · 0 chunks · sources memory · plugin memory-core · vector unknown · fts ready · cache on  │
│                 │ (0)                                                                                               │
│ Probes          │ enabled                                                                                           │
│ Events          │ none                                                                                              │
│ Heartbeat       │ 30m (main)                                                                                        │
│ Last heartbeat  │ skipped · 11m ago ago · unknown                                                                   │
│ Sessions        │ 19 active · default gpt-5.3-codex (272k ctx) · ~/.openclaw/agents/main/sessions/sessions.json     │
└─────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────┘

Security audit
Summary: 0 critical · 2 warn · 1 info
  WARN Reverse proxy headers are not trusted
    gateway.bind is loopback and gateway.trustedProxies is empty. If you expose the Control UI through a reverse proxy, configure trusted proxies so local-client c…
    Fix: Set gateway.trustedProxies to your proxy IPs or keep the Control UI local-only.
  WARN Signal DMs share the main session
    Multiple DM senders currently share the main session, which can leak context across users.
    Fix: Run: openclaw config set session.dmScope "per-channel-peer" (or "per-account-channel-peer" for multi-account channels) to isolate DM sessions per sender.
Full report: openclaw security audit
Deep probe: openclaw security audit --deep

Channels
┌──────────┬─────────┬────────┬───────────────────────────────────────────────────────────────────────────────────────┐
│ Channel  │ Enabled │ State  │ Detail                                                                                │
├──────────┼─────────┼────────┼───────────────────────────────────────────────────────────────────────────────────────┤
│ Signal   │ ON      │ OK     │ configured                                                                            │
└──────────┴─────────┴────────┴───────────────────────────────────────────────────────────────────────────────────────┘

Sessions
┌────────────────────────────────────────┬────────┬─────────┬──────────────────────┬──────────────────────────────────┐
│ Key                                    │ Kind   │ Age     │ Model                │ Tokens                           │
├────────────────────────────────────────┼────────┼─────────┼──────────────────────┼──────────────────────────────────┤
│ agent:main:main                        │ direct │ 1m ago  │ gpt-5.3-codex        │ 15k/272k (6%) · 🗄️ 156% cached   │
│ agent:main:cron:65aa3a2e-0245-4…       │ direct │ 30h ago │ minimax/minimax-m2.5 │ 11k/197k (5%) · 🗄️ 7% cached     │
│ agent:main:cron:ef27feba-f748-4…       │ direct │ 30h ago │ minimax/minimax-m2.5 │ 14k/197k (7%) · 🗄️ 1084% cached  │
│ agent:main:cron:ef27feba-f748-4…       │ direct │ 30h ago │ minimax/minimax-m2.5 │ 14k/197k (7%) · 🗄️ 1084% cached  │
│ agent:main:cron:42bff234-f7d1-4…       │ direct │ 41h ago │ auto                 │ 34k/2000k (2%)                   │
│ agent:main:cron:42bff234-f7d1-4…       │ direct │ 41h ago │ auto                 │ 34k/2000k (2%)                   │
│ agent:main:cron:c8848a64-041d-4…       │ direct │ 42h ago │ coder-model          │ 22k/128k (17%)                   │
│ agent:main:cron:c8848a64-041d-4…       │ direct │ 42h ago │ coder-model          │ 22k/128k (17%)                   │
│ agent:main:cron:eb59675f-9f3f-4…       │ direct │ 43h ago │ auto                 │ 7.6k/2000k (0%) · 🗄️ 149% cached │
│ agent:main:cron:eb59675f-9f3f-4…       │ direct │ 43h ago │ auto                 │ 7.6k/2000k (0%) · 🗄️ 149% cached │
└────────────────────────────────────────┴────────┴─────────┴──────────────────────┴──────────────────────────────────┘

Health
┌──────────┬───────────┬──────────────────────────────────────────────────────────────────────────────────────────────┐
│ Item     │ Status    │ Detail                                                                                       │
├──────────┼───────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ Gateway  │ reachable │ 1ms                                                                                          │
│ Signal   │ OK        │ ok (default:default:1ms)                                                                     │
└──────────┴───────────┴──────────────────────────────────────────────────────────────────────────────────────────────┘

FAQ: https://docs.openclaw.ai/faq
Troubleshooting: https://docs.openclaw.ai/troubleshooting

Next steps:
  Need to share?      openclaw status --all
  Need to debug live? openclaw logs --follow
  Need to test channels? openclaw status --deep

## Process list top CPU
username          5782   9.4  3.0 1890815136 497280   ??  S    Mon01PM  53:59.16 /Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/145.0.7632.109/Helpers/Google Chrome Helper (Renderer).app/Contents/MacOS/Google Chrome Helper (Renderer) --type=renderer --lang=ja --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=64 --time-ticks-at-unix-epoch=-1771816820129959 --launch-time-ticks=2589075013 --shared-files --metrics-shmem-handle=1752395122,r,4574459358746070254,13493310839733776629,2097152 --field-trial-handle=1718379636,r,14975098752248561181,6490813651554920531,262144 --variations-seed-version=20260222-030036.739000-production --trace-process-track-uuid=3190709046282549830 --seatbelt-client=73
username         15030   1.5  4.0 445222512 678288   ??  S     8:41AM   0:37.02 openclaw-gateway     
_driverkit         523   0.8  0.3 435304960  42928   ??  Ss   Mon12PM   3:57.71 /System/Library/DriverExtensions/com.apple.DriverKit-AppleBCMWLAN.dext/com.apple.DriverKit-AppleBCMWLAN com.apple.bcmwlan 0x100000ce2 com.apple.DriverKit-AppleBCMWLAN
root               416   0.4  0.2 435380384  28336   ??  Ss   Mon12PM   7:55.07 /usr/libexec/airportd
username          1027   0.2  1.7 1650424096 286912   ??  S    Mon12PM   5:28.03 /Applications/Postman.app/Contents/Frameworks/Postman Helper (Renderer).app/Contents/MacOS/Postman Helper (Renderer) --type=renderer --user-data-dir=/Users/username/Library/Application Support/Postman --app-path=/Applications/Postman.app/Contents/Resources/app.asar --no-sandbox --no-zygote --lang=en-US --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=7 --time-ticks-at-unix-epoch=-1771816820129456 --launch-time-ticks=59671199 --shared-files --field-trial-handle=1718379636,r,5079896452471728040,2752563536170496506,262144 --enable-features=ScreenCaptureKitPickerScreen,ScreenCaptureKitStreamPickerSonoma --disable-features=MacWebContentsOcclusion,SpareRendererForSitePerProcess,TimeoutHangingVideoCaptureStarts --variations-seed-version
username           633   0.2  1.4 1649164256 234304   ??  S    Mon12PM   1:01.25 /Applications/Postman.app/Contents/MacOS/Postman
username          1055   0.1  2.5 1896097136 425120   ??  S    Mon12PM   4:30.83 /Applications/Discord.app/Contents/Frameworks/Discord Helper (Renderer).app/Contents/MacOS/Discord Helper (Renderer) --type=renderer --user-data-dir=/Users/username/Library/Application Support/discord --standard-schemes=disclip --secure-schemes=disclip,sentry-ipc --bypasscsp-schemes=sentry-ipc --cors-schemes=sentry-ipc --fetch-schemes=disclip,sentry-ipc --streaming-schemes=disclip --app-path=/Applications/Discord.app/Contents/Resources/app.asar --no-sandbox --no-zygote --enable-blink-features=EnumerateDevices,AudioOutputDevices --autoplay-policy=no-user-gesture-required --lang=en-US --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=6 --time-ticks-at-unix-epoch=-1771816820133617 --launch-time-ticks=68038190 --shared-files --field-trial-handle=1718379636,r,14058496808204291326,15290222828867150131,262144 --enable-features=ScreenCaptureKitPickerScreen,ScreenCaptureKitStreamPickerSonoma --disable-features=AllowAggressiveThrottlingWithWebSocket,HardwareMediaKeyHandling,IntensiveWakeUpThrottling,MacWebContentsOcclusion,MediaSessionService,ScreenAIOCREnabled,SpareRendererForSitePerProcess,TimeoutHangingVideoCaptureStarts,UseEcoQoSForBackgroundProcess,WinRetrieveSuggestionsOnlyOnDemand --variations-seed-version --enable-node-leakage-in-renderers
username           637   0.1  2.5 537463648 418560   ??  S    Mon12PM   2:55.55 /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
root               330   0.1  0.3 435489968  53376   ??  Ss   Mon12PM   1:06.36 /usr/libexec/logd
_networkd          446   0.1  0.1 435906816  21248   ??  Ss   Mon12PM   0:33.88 /usr/libexec/symptomsd
username         19671   0.0  0.0 435300096   1184   ??  S     1:54PM   0:00.00 head -n 80
username         19670   0.0  0.0 435300384   1232   ??  S     1:54PM   0:00.00 sort -nr -k3
username         19666   0.0  0.0 435300112   1824   ??  S     1:54PM   0:00.01 bash -lc ps aux | sort -nr -k3 | head -n 80
username         19665   0.0  0.0 435308528   2224   ??  Ss    1:54PM   0:00.01 /bin/zsh -c set -euo pipefail\012TASK_DIR="/Users/username/.openclaw/workspace/work/2026/0224-1353_mac-security-audit"\012run(){ echo "\n## $1\n\`\`\`" >> "$TASK_DIR/LOG.md"; bash -lc "$2" >> "$TASK_DIR/LOG.md" 2>&1 || true; echo "\`\`\`" >> "$TASK_DIR/LOG.md"; }\012run "Process list top CPU" "ps aux | sort -nr -k3 | head -n 80"\012run "Process list top MEM" "ps aux | sort -nr -k4 | head -n 80"\012run "Unsigned / ad-hoc apps in /Applications" "system_profiler SPApplicationsDataType | egrep -A4 'Location:|Signed by:|Obtained from:' | head -n 400"\012run "Recent install history" "tail -n 200 /Library/Receipts/InstallHistory.plist 2>/dev/null; softwareupdate --history | tail -n 80"\012run "launchctl suspicious grep" "launchctl list | egrep -vi 'com.apple|com.google|ai.openclaw|homebrew|org.chromium' | head -n 200"\012run "user startup items" "osascript -e 'tell application \"System Events\" to get the name of every login item'"\012run "SSH config quick" "grep -v '^#' /etc/ssh/sshd_config 2>/dev/null | sed '/^$/d'; ls -la /Users/username/.ssh 2>/dev/null; ls -la /Users/username/.ssh/authorized_keys 2>/dev/null"\012run "TCC / Full disk access grants (metadata only)" "sqlite3 \"$HOME/Library/Application Support/com.apple.TCC/TCC.db\" 'select service,client,auth_value,last_modified from access order by last_modified desc limit 80;'"\012run "Quarantine disabled flags check" "defaults read com.apple.LaunchServices LSQuarantine 2>/dev/null || echo 'LSQuarantine key not set (default on)'; spctl --status"\012\012echo done
username         19658   0.0  0.2 435374464  26400   ??  S     1:54PM   0:00.10 /System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/Metadata.framework/Versions/A/Support/mdworker_shared -s mdworker -c MDSImporterWorker -m com.apple.mdworker.shared
username         19416   0.0  0.1 435373840  19664   ??  S     1:53PM   0:00.08 /System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/Metadata.framework/Versions/A/Support/mdworker_shared -s mdworker -c MDSImporterWorker -m com.apple.mdworker.shared
username         18164   0.0  0.6 1890520944 105488   ??  S    12:23PM   0:00.16 /Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/145.0.7632.109/Helpers/Google Chrome Helper (Renderer).app/Contents/MacOS/Google Chrome Helper (Renderer) --type=renderer --lang=ja --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=269 --time-ticks-at-unix-epoch=-1771816820129959 --launch-time-ticks=36136690283 --shared-files --metrics-shmem-handle=1752395122,r,5314389696395082517,11309594151024963937,2097152 --field-trial-handle=1718379636,r,14975098752248561181,6490813651554920531,262144 --variations-seed-version=20260222-030036.739000-production --trace-process-track-uuid=3190709238376128875 --seatbelt-client=159
username         18087   0.0  0.1 435361840  23648   ??  S    12:21PM   0:00.18 /System/Library/PrivateFrameworks/AvatarPersistence.framework/Support/avatarsd
username         18086   0.0  0.3 440001568  49200   ??  S    12:21PM   0:00.29 /System/Library/PrivateFrameworks/Noticeboard.framework/Versions/A/Resources/nbagent.app/Contents/MacOS/nbagent
username         17091   0.0  0.2 507347648  38576   ??  Ss   11:10AM   0:00.08 /System/Library/Frameworks/WebKit.framework/Versions/A/XPCServices/com.apple.WebKit.WebContent.xpc/Contents/MacOS/com.apple.WebKit.WebContent
username         15713   0.0  0.5 486085728  87648   ??  S     9:27AM   0:01.09 /Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/145.0.7632.109/Helpers/Google Chrome Helper (Alerts).app/Contents/MacOS/Google Chrome Helper (Alerts) --type=utility --utility-sub-type=mac_notifications.mojom.MacNotificationProvider --lang=ja --service-sandbox-type=none --message-loop-type-ui --shared-files --metrics-shmem-handle=1752395122,r,7600965871101911936,3481376327064934229,524288 --field-trial-handle=1718379636,r,14975098752248561181,6490813651554920531,262144 --variations-seed-version=20260222-030036.739000-production --trace-process-track-uuid=3190709194335161972
username         15054   0.0  1.4 441344608 230272   ??  S     8:41AM   0:20.87 /opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home/bin/java --enable-native-access=ALL-UNNAMED -classpath /opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/signal-cli-0.13.24.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/libsignal-cli-0.13.24.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/libsignal-client-0.87.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/bcprov-jdk18on-1.83.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/jackson-core-2.20.1.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/signal-service-java-2.15.3_unofficial_137.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/jackson-module-kotlin-2.20.1.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/jackson-databind-2.20.1.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/argparse4j-0.9.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/dbus-java-transport-native-unixsocket-5.0.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/jul-to-slf4j-2.0.17.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/logback-classic-1.5.25.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/dbus-java-core-5.0.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/HikariCP-7.0.2.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/slf4j-api-2.0.17.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/jackson-annotations-2.20.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/logback-core-1.5.25.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/sqlite-jdbc-3.51.1.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/jsr305-3.0.2.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/models-jvm-2.15.3_unofficial_137.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/util-jvm-2.15.3_unofficial_137.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/rxkotlin-3.0.1.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/wire-runtime-jvm-4.9.11.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/kotlinx-coroutines-core-jvm-1.9.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/kotlin-stdlib-jdk7-2.1.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/okhttp-jvm-5.3.2.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/kotlin-reflect-2.1.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/kotlinx-serialization-core-jvm-1.9.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/kotlinx-serialization-json-jvm-1.9.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/okio-jvm-3.16.4.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/kotlin-stdlib-2.2.21.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/kotlin-stdlib-jdk8-2.1.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/libphonenumber-8.13.50.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/rxjava-3.0.13.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/annotations-23.0.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/reactive-streams-1.0.3.jar org.asamk.signal.Main -a +8613089441211 daemon --http 127.0.0.1:8080 --no-receive-stdout
username         15028   0.0  0.3 436165824  42304   ??  S     8:41AM   0:00.30 openclaw    
username         13772   0.0  0.0 435322608   6832   ??  S     8:36AM   0:00.09 /usr/libexec/seserviced
username         12303   0.0  0.3 507450768  57760   ??  Ss    8:33AM   0:00.39 /System/Library/Frameworks/WebKit.framework/Versions/A/XPCServices/com.apple.WebKit.WebContent.xpc/Contents/MacOS/com.apple.WebKit.WebContent
username         11906   0.0  0.1 435410896  14864   ??  Ss    8:32AM   0:00.05 /System/Library/Frameworks/Metal.framework/Versions/A/XPCServices/MTLCompilerService.xpc/Contents/MacOS/MTLCompilerService
username         11729   0.0  0.1 435368816  16064   ??  S     7:20AM   0:00.52 /System/Library/PrivateFrameworks/JetCore.framework/Support/jetpackassetd
username         11335   0.0  0.1 435310624   9136   ??  S<    3:10AM   0:00.04 /Applications/Discord.app/Contents/Frameworks/Squirrel.framework/Resources/ShipIt com.hnc.Discord.ShipIt /Users/username/Library/Caches/com.hnc.Discord.ShipIt/ShipItState.plist
username         11296   0.0  0.2 435376608  27488   ??  S     2:52AM   0:01.08 /usr/libexec/remindd
username         10947   0.0  0.1 435390304  17360   ??  S    12:45AM   0:00.32 /System/Library/CoreServices/Keychain Circle Notification.app/Contents/MacOS/Keychain Circle Notification
username         10939   0.0  0.0 435354784   7248   ??  S    12:45AM   0:00.05 /System/Library/CoreServices/EscrowSecurityAlert.app/Contents/MacOS/EscrowSecurityAlert
username         10883   0.0  0.0 435363072   6752   ??  S    12:27AM   0:00.07 /System/Library/PrivateFrameworks/AMPLibrary.framework/Versions/A/Support/AMPArtworkAgent --launchd
username         10882   0.0  0.0 435357008   4784   ??  S    12:27AM   0:00.07 /System/Library/PrivateFrameworks/BookKit.framework/Versions/A/XPCServices/com.apple.BKAgentService.xpc/Contents/MacOS/com.apple.BKAgentService
username         10881   0.0  0.0 435357424   6880   ??  S    12:27AM   0:00.11 /System/Library/PrivateFrameworks/PodcastServices.framework/XPCServices/PodcastContentService.xpc/Contents/MacOS/PodcastContentService
username         10877   0.0  0.2 435397504  29152   ??  S    12:27AM   0:00.78 /System/Library/PrivateFrameworks/AMPLibrary.framework/Versions/A/Support/AMPLibraryAgent --launchd
username         10876   0.0  0.0 435383088   7792   ??  Ss   12:27AM   0:00.06 /System/Library/PrivateFrameworks/AssistantServices.framework/Versions/A/XPCServices/media-indexer.xpc/Contents/MacOS/media-indexer
username         10845   0.0  0.1 435355744  10784   ??  S    12:26AM   0:00.09 /System/Library/PrivateFrameworks/IMDPersistence.framework/IMAutomaticHistoryDeletionAgent.app/Contents/MacOS/IMAutomaticHistoryDeletionAgent
username         10844   0.0  0.1 435357728  10432   ??  S    12:26AM   0:00.29 /System/Library/PrivateFrameworks/Categories.framework/Versions/A/XPCServices/CategoriesService.xpc/Contents/MacOS/CategoriesService
username         10182   0.0  0.2 435568912  26848   ??  Ss    5:44PM   0:00.10 /System/Library/CoreServices/ControlCenter.app/Contents/PlugIns/DisplayControls.appex/Contents/MacOS/DisplayControls -LaunchArguments eyJzZXJ2aWNlTmFtZSI6ImNvbS5hcHBsZS5jb250cm9scy5kaXNwbGF5IiwidHlwZSI6MSwiZW5oYW5jZWRTZWN1cml0eSI6ZmFsc2V9
username         10180   0.0  0.1 435355584   9424   ??  Ss    5:44PM   0:00.06 /System/Library/Frameworks/ExtensionFoundation.framework/Versions/A/XPCServices/extensionkitservice.xpc/Contents/MacOS/extensionkitservice
username         10165   0.0  0.1 435344432   8448   ??  Ss    5:44PM   0:00.13 /System/Library/PrivateFrameworks/CloudTelemetry.framework/Versions/A/XPCServices/CloudTelemetryService.xpc/Contents/MacOS/CloudTelemetryService
username          9754   0.0  0.1 435357088   8448   ??  S     5:02PM   0:00.08 /usr/libexec/ciphermld
username          9719   0.0  0.1 435362272  11600   ??  S     5:01PM   0:00.16 /System/Library/PrivateFrameworks/MapsSync.framework/mapssyncd
username          9712   0.0  0.0 435355072   7264   ??  S     5:01PM   0:00.18 /System/Library/PrivateFrameworks/DeviceCheckInternal.framework/devicecheckd
username          9555   0.0  0.0 435306608   3632   ??  Ss    4:49PM   0:00.09 /System/Library/PrivateFrameworks/RemoteManagement.framework/XPCServices/ManagedSettingsSubscriber.xpc/Contents/MacOS/ManagedSettingsSubscriber
username          9554   0.0  0.0 435339056   6208   ??  Ss    4:49PM   0:00.09 /System/Library/PrivateFrameworks/RemoteManagement.framework/XPCServices/ASConfigurationSubscriber.xpc/Contents/MacOS/ASConfigurationSubscriber
username          9553   0.0  0.0 435305024   3248   ??  Ss    4:49PM   0:00.08 /System/Library/PrivateFrameworks/RemoteManagement.framework/XPCServices/ManagementTestSubscriber.xpc/Contents/MacOS/ManagementTestSubscriber
username          9552   0.0  0.0 435306016   3792   ??  Ss    4:49PM   0:00.08 /System/Library/PrivateFrameworks/RemoteManagement.framework/XPCServices/ManagedAppsSubscriber.xpc/Contents/MacOS/ManagedAppsSubscriber
username          9551   0.0  0.0 435305536   4560   ??  Ss    4:49PM   0:00.09 /System/Library/PrivateFrameworks/RemoteManagement.framework/XPCServices/AccountSubscriber.xpc/Contents/MacOS/AccountSubscriber
username          9550   0.0  0.0 435305200   3216   ??  Ss    4:49PM   0:00.08 /System/Library/PrivateFrameworks/RemoteManagement.framework/XPCServices/PasscodeSettingsSubscriber.xpc/Contents/MacOS/PasscodeSettingsSubscriber
username          9549   0.0  0.0 435305632   3216   ??  Ss    4:49PM   0:00.08 /System/Library/PrivateFrameworks/RemoteManagement.framework/XPCServices/LegacyProfilesSubscriber.xpc/Contents/MacOS/LegacyProfilesSubscriber
username          9545   0.0  0.0 435305568   5136   ??  Ss    4:49PM   0:00.10 /System/Library/PrivateFrameworks/RemoteManagement.framework/XPCServices/ScreenSharingSubscriber.xpc/Contents/MacOS/ScreenSharingSubscriber
username          9544   0.0  0.0 435305472   3232   ??  Ss    4:49PM   0:00.07 /System/Library/PrivateFrameworks/RemoteManagement.framework/XPCServices/InteractiveLegacyProfilesSubscriber.xpc/Contents/MacOS/InteractiveLegacyProfilesSubscriber
username          9543   0.0  0.0 435305280   3312   ??  Ss    4:49PM   0:00.08 /System/Library/PrivateFrameworks/RemoteManagement.framework/XPCServices/SecuritySubscriber.xpc/Contents/MacOS/SecuritySubscriber
username          9542   0.0  0.0 435339328   6080   ??  Ss    4:49PM   0:00.05 /System/Library/PrivateFrameworks/SafariFoundation.framework/Versions/A/XPCServices/SafariConfigurationSubscriber.xpc/Contents/MacOS/SafariConfigurationSubscriber
username          9541   0.0  0.0 435356832   6224   ??  S     4:49PM   0:00.11 /System/Library/PrivateFrameworks/RemoteManagement.framework/RemoteManagementAgent
username          9176   0.0  0.0 435358208   7232   ??  S     4:23PM   0:00.06 cloudphotod
username          9140   0.0  0.0 435345088   7744   ??  Ss    4:20PM   0:00.16 /System/Library/PrivateFrameworks/CloudTelemetry.framework/Versions/A/XPCServices/CloudTelemetryService.xpc/Contents/MacOS/CloudTelemetryService
username          8816   0.0  0.0 435356288   7664   ??  S     3:54PM   0:00.13 /usr/libexec/proactiveeventtrackerd
username          8146   0.0  0.1 435360112  12592   ??  S     3:03PM   0:00.19 /System/Library/PrivateFrameworks/PrivateCloudCompute.framework/privatecloudcomputed.app/Contents/MacOS/privatecloudcomputed
username          8095   0.0  0.0 435355344   8048   ??  Ss    3:00PM   0:00.03 /System/Library/Frameworks/Intents.framework/XPCServices/intents_helper.xpc/Contents/MacOS/intents_helper
username          7453   0.0  0.1 435349424  11904   ??  S     2:39PM   0:00.58 /usr/libexec/filevaultd
username          7452   0.0  0.1 435356928  15088   ??  S     2:39PM   0:00.13 /System/Library/PrivateFrameworks/GeoAnalytics.framework/geoanalyticsd
username          7284   0.0  0.0 435318416   5680   ??  S     2:23PM   0:00.04 /usr/libexec/backgroundassets.user
username          7283   0.0  0.0 435361088   7040   ??  S     2:23PM   0:00.15 /usr/libexec/dprivacyd
username          7011   0.0  2.3 1890832416 392688   ??  S    Mon01PM   1:04.59 /Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/145.0.7632.109/Helpers/Google Chrome Helper (Renderer).app/Contents/MacOS/Google Chrome Helper (Renderer) --type=renderer --lang=ja --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=108 --time-ticks-at-unix-epoch=-1771816820129959 --launch-time-ticks=5626748346 --shared-files --metrics-shmem-handle=1752395122,r,7042603934695387351,15723167631753956257,2097152 --field-trial-handle=1718379636,r,14975098752248561181,6490813651554920531,262144 --variations-seed-version=20260222-030036.739000-production --trace-process-track-uuid=3190709087512391186 --seatbelt-client=162
username          6991   0.0  0.0 435316960   2656   ??  S    Mon01PM   0:00.01 /System/Library/Frameworks/ColorSync.framework/Support/colorsync.useragent
username          6935   0.0  0.1 435362432  18816   ??  S    Mon01PM   0:00.64 /System/Library/Frameworks/ManagedAppDistribution.framework/Support/managedappdistributionagent
username          6923   0.0  0.0 435343824   7392   ??  Ss   Mon01PM   0:00.19 /System/Library/PrivateFrameworks/MediaAnalysisAccess.framework/Versions/A/XPCServices/mediaanalysisd-access.xpc/Contents/MacOS/mediaanalysisd-access
username          6914   0.0  0.0 435305360   3776   ??  S    Mon01PM   0:00.04 /Library/Apple/System/Library/CoreServices/XProtect.app/Contents/MacOS/XProtect
username          6902   0.0  0.1 435901696  10544   ??  S    Mon01PM   0:00.14 /System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/Metadata.framework/Versions/A/Support/managedcorespotlightd
username          6884   0.0  0.0 435322016   3696   ??  S    Mon01PM   0:00.06 /usr/libexec/mlruntimed
username          6704   0.0  0.0 435356864   7424   ??  S    Mon01PM   0:00.10 /usr/libexec/metrickitd
username          6679   0.0  0.1 435355424   8416   ??  Ss   Mon01PM   0:00.10 /System/Library/PrivateFrameworks/ManagedBackgroundAssets.framework/Versions/A/XPCServices/Managed Background Assets Helper Service.xpc/Contents/MacOS/Managed Background Assets Helper Service
username          6194   0.0  0.0 435321312   7296   ??  S    Mon01PM   0:00.09 /System/Library/PrivateFrameworks/ProtectedCloudStorage.framework/Helpers/ProtectedCloudKeySyncing
username          5754   0.0  0.1 435321680  11520   ??  Ss   Mon01PM   0:02.59 /System/Library/Frameworks/VideoToolbox.framework/Versions/A/XPCServices/VTDecoderXPCService.xpc/Contents/MacOS/VTDecoderXPCService
username          5333   0.0  0.1 435366288  15504   ??  Ss   Mon12PM   0:04.81 /System/Library/Frameworks/ExtensionFoundation.framework/Versions/A/XPCServices/extensionkitservice.xpc/Contents/MacOS/extensionkitservice
username          5323   0.0  0.1 435359296  16144   ??  S    Mon12PM   0:00.19 /System/Library/PrivateFrameworks/IntelligencePlatformCore.framework/Versions/A/intelligenceplatformd
username          4484   0.0  0.2 435410144  25440   ??  S    Mon12PM   0:00.48 /usr/libexec/studentd
username          4010   0.0  0.0 435382384   6256   ??  Ss   Mon12PM   0:00.03 /System/Library/Frameworks/Metal.framework/Versions/A/XPCServices/MTLCompilerService.xpc/Contents/MacOS/MTLCompilerService

## Process list top MEM
username         15030   6.0  4.0 445222512 678288   ??  S     8:41AM   0:37.02 openclaw-gateway     
username          5782   8.7  3.0 1890815136 497280   ??  S    Mon01PM  53:59.17 /Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/145.0.7632.109/Helpers/Google Chrome Helper (Renderer).app/Contents/MacOS/Google Chrome Helper (Renderer) --type=renderer --lang=ja --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=64 --time-ticks-at-unix-epoch=-1771816820129959 --launch-time-ticks=2589075013 --shared-files --metrics-shmem-handle=1752395122,r,4574459358746070254,13493310839733776629,2097152 --field-trial-handle=1718379636,r,14975098752248561181,6490813651554920531,262144 --variations-seed-version=20260222-030036.739000-production --trace-process-track-uuid=3190709046282549830 --seatbelt-client=73
username          1055   0.1  2.5 1896097136 425120   ??  S    Mon12PM   4:30.83 /Applications/Discord.app/Contents/Frameworks/Discord Helper (Renderer).app/Contents/MacOS/Discord Helper (Renderer) --type=renderer --user-data-dir=/Users/username/Library/Application Support/discord --standard-schemes=disclip --secure-schemes=disclip,sentry-ipc --bypasscsp-schemes=sentry-ipc --cors-schemes=sentry-ipc --fetch-schemes=disclip,sentry-ipc --streaming-schemes=disclip --app-path=/Applications/Discord.app/Contents/Resources/app.asar --no-sandbox --no-zygote --enable-blink-features=EnumerateDevices,AudioOutputDevices --autoplay-policy=no-user-gesture-required --lang=en-US --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=6 --time-ticks-at-unix-epoch=-1771816820133617 --launch-time-ticks=68038190 --shared-files --field-trial-handle=1718379636,r,14058496808204291326,15290222828867150131,262144 --enable-features=ScreenCaptureKitPickerScreen,ScreenCaptureKitStreamPickerSonoma --disable-features=AllowAggressiveThrottlingWithWebSocket,HardwareMediaKeyHandling,IntensiveWakeUpThrottling,MacWebContentsOcclusion,MediaSessionService,ScreenAIOCREnabled,SpareRendererForSitePerProcess,TimeoutHangingVideoCaptureStarts,UseEcoQoSForBackgroundProcess,WinRetrieveSuggestionsOnlyOnDemand --variations-seed-version --enable-node-leakage-in-renderers
username           637   0.3  2.5 537463648 418560   ??  S    Mon12PM   2:55.55 /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
username          7011   0.8  2.3 1890832416 392688   ??  S    Mon01PM   1:04.59 /Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/145.0.7632.109/Helpers/Google Chrome Helper (Renderer).app/Contents/MacOS/Google Chrome Helper (Renderer) --type=renderer --lang=ja --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=108 --time-ticks-at-unix-epoch=-1771816820129959 --launch-time-ticks=5626748346 --shared-files --metrics-shmem-handle=1752395122,r,7042603934695387351,15723167631753956257,2097152 --field-trial-handle=1718379636,r,14975098752248561181,6490813651554920531,262144 --variations-seed-version=20260222-030036.739000-production --trace-process-track-uuid=3190709087512391186 --seatbelt-client=162
username          1027   0.2  1.7 1650424096 286912   ??  S    Mon12PM   5:28.04 /Applications/Postman.app/Contents/Frameworks/Postman Helper (Renderer).app/Contents/MacOS/Postman Helper (Renderer) --type=renderer --user-data-dir=/Users/username/Library/Application Support/Postman --app-path=/Applications/Postman.app/Contents/Resources/app.asar --no-sandbox --no-zygote --lang=en-US --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=7 --time-ticks-at-unix-epoch=-1771816820129456 --launch-time-ticks=59671199 --shared-files --field-trial-handle=1718379636,r,5079896452471728040,2752563536170496506,262144 --enable-features=ScreenCaptureKitPickerScreen,ScreenCaptureKitStreamPickerSonoma --disable-features=MacWebContentsOcclusion,SpareRendererForSitePerProcess,TimeoutHangingVideoCaptureStarts --variations-seed-version
username         15054   0.0  1.4 441344608 230272   ??  S     8:41AM   0:20.87 /opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home/bin/java --enable-native-access=ALL-UNNAMED -classpath /opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/signal-cli-0.13.24.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/libsignal-cli-0.13.24.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/libsignal-client-0.87.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/bcprov-jdk18on-1.83.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/jackson-core-2.20.1.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/signal-service-java-2.15.3_unofficial_137.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/jackson-module-kotlin-2.20.1.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/jackson-databind-2.20.1.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/argparse4j-0.9.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/dbus-java-transport-native-unixsocket-5.0.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/jul-to-slf4j-2.0.17.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/logback-classic-1.5.25.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/dbus-java-core-5.0.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/HikariCP-7.0.2.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/slf4j-api-2.0.17.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/jackson-annotations-2.20.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/logback-core-1.5.25.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/sqlite-jdbc-3.51.1.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/jsr305-3.0.2.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/models-jvm-2.15.3_unofficial_137.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/util-jvm-2.15.3_unofficial_137.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/rxkotlin-3.0.1.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/wire-runtime-jvm-4.9.11.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/kotlinx-coroutines-core-jvm-1.9.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/kotlin-stdlib-jdk7-2.1.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/okhttp-jvm-5.3.2.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/kotlin-reflect-2.1.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/kotlinx-serialization-core-jvm-1.9.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/kotlinx-serialization-json-jvm-1.9.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/okio-jvm-3.16.4.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/kotlin-stdlib-2.2.21.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/kotlin-stdlib-jdk8-2.1.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/libphonenumber-8.13.50.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/rxjava-3.0.13.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/annotations-23.0.0.jar:/opt/homebrew/Cellar/signal-cli/0.13.24/libexec/lib/reactive-streams-1.0.3.jar org.asamk.signal.Main -a +8613089441211 daemon --http 127.0.0.1:8080 --no-receive-stdout
username           633   0.1  1.4 1649164256 234304   ??  S    Mon12PM   1:01.25 /Applications/Postman.app/Contents/MacOS/Postman
username          3973   0.0  1.3 1890627424 222768   ??  S    Mon12PM   0:03.06 /Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/145.0.7632.109/Helpers/Google Chrome Helper (Renderer).app/Contents/MacOS/Google Chrome Helper (Renderer) --type=renderer --lang=ja --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=34 --time-ticks-at-unix-epoch=-1771816820129959 --launch-time-ticks=1135017335 --shared-files --metrics-shmem-handle=1752395122,r,4747847168685327314,4685300312116049545,2097152 --field-trial-handle=1718379636,r,14975098752248561181,6490813651554920531,262144 --variations-seed-version=20260222-030036.739000-production --trace-process-track-uuid=3190709018171294360 --seatbelt-client=162
username          1005   0.0  1.3 1891060960 216416   ??  S    Mon12PM   1:41.31 /Applications/Discord.app/Contents/MacOS/Discord
username           792   0.0  1.0 486435440 172192   ??  S    Mon12PM   3:29.71 /Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/145.0.7632.109/Helpers/Google Chrome Helper.app/Contents/MacOS/Google Chrome Helper --type=gpu-process --gpu-preferences=SAAAAAAAAAAgAQQEAAAAAAAAAAAAAGAAAwAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAACAAAAAAAAAAIAAAAAAAAAA== --shared-files --metrics-shmem-handle=1752395122,r,366515796883784244,16763569671639602547,262144 --field-trial-handle=1718379636,r,14975098752248561181,6490813651554920531,262144 --variations-seed-version=20260222-030036.739000-production --trace-process-track-uuid=3190708988185955192 --seatbelt-client=22
username          3091   0.0  0.9 440490032 150016   ??  S    Mon12PM   0:09.61 /System/Volumes/Preboot/Cryptexes/App/System/Applications/Safari.app/Contents/MacOS/Safari
username          1615   0.0  0.9 436219376 156624   ??  Ss   Mon12PM   0:13.32 /System/Library/Input Methods/JapaneseIM-RomajiTyping.app/Contents/PlugIns/JapaneseIM-RomajiTyping.appex/Contents/MacOS/JapaneseIM-RomajiTyping -AppleLanguages ("ja-JP")
username           643   0.0  0.9 436312176 147200   ??  S    Mon12PM   0:46.77 /Applications/Ghostty.app/Contents/MacOS/ghostty
username           804   0.0  0.8 1890596752 141936   ??  S    Mon12PM   0:00.99 /Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/145.0.7632.109/Helpers/Google Chrome Helper (Renderer).app/Contents/MacOS/Google Chrome Helper (Renderer) --type=renderer --lang=ja --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=5 --time-ticks-at-unix-epoch=-1771816820129959 --launch-time-ticks=37502503 --shared-files --metrics-shmem-handle=1752395122,r,11257191504216604452,13874606482759529877,2097152 --field-trial-handle=1718379636,r,14975098752248561181,6490813651554920531,262144 --variations-seed-version=20260222-030036.739000-production --trace-process-track-uuid=3190708990997080739 --seatbelt-client=26
username           770   0.0  0.8 435807856 130384   ??  S    Mon12PM   0:07.71 /System/Library/CoreServices/Spotlight.app/Contents/MacOS/Spotlight
username           764   0.0  0.8 435505664 138560   ??  S    Mon12PM   0:16.01 /System/Library/PrivateFrameworks/MediaAnalysis.framework/Versions/A/mediaanalysisd
username           694   0.0  0.8 445333104 133552   ??  S    Mon12PM   1:32.51 /System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/Metadata.framework/Versions/A/Support/corespotlightd
username           406   0.0  0.8 435822288 129952   ??  Ss   Mon12PM   2:44.56 /System/Library/CoreServices/loginwindow.app/Contents/MacOS/loginwindow console
username          1431   0.0  0.7 1892274688 118480   ??  S    Mon12PM   0:01.99 /Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/145.0.7632.109/Helpers/Google Chrome Helper (Renderer).app/Contents/MacOS/Google Chrome Helper (Renderer) --type=renderer --extension-process --lang=ja --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=13 --time-ticks-at-unix-epoch=-1771816820129959 --launch-time-ticks=78959291 --shared-files --metrics-shmem-handle=1752395122,r,16244881359942501864,4567639586751513491,2097152 --field-trial-handle=1718379636,r,14975098752248561181,6490813651554920531,262144 --variations-seed-version=20260222-030036.739000-production --trace-process-track-uuid=3190708998493415531 --seatbelt-client=122
username           793   0.6  0.7 486136512 114912   ??  S    Mon12PM   0:47.91 /Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/145.0.7632.109/Helpers/Google Chrome Helper.app/Contents/MacOS/Google Chrome Helper --type=utility --utility-sub-type=network.mojom.NetworkService --lang=ja --service-sandbox-type=network --shared-files --metrics-shmem-handle=1752395122,r,7474906329494407307,1434400516860548351,524288 --field-trial-handle=1718379636,r,14975098752248561181,6490813651554920531,262144 --variations-seed-version=20260222-030036.739000-production --trace-process-track-uuid=3190708989122997041 --seatbelt-client=22
username         18164   0.0  0.6 1890520944 105488   ??  S    12:23PM   0:00.16 /Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/145.0.7632.109/Helpers/Google Chrome Helper (Renderer).app/Contents/MacOS/Google Chrome Helper (Renderer) --type=renderer --lang=ja --num-raster-threads=4 --enable-zero-copy --enable-gpu-memory-buffer-compositor-resources --enable-main-frame-before-activation --renderer-client-id=269 --time-ticks-at-unix-epoch=-1771816820129959 --launch-time-ticks=36136690283 --shared-files --metrics-shmem-handle=1752395122,r,5314389696395082517,11309594151024963937,2097152 --field-trial-handle=1718379636,r,14975098752248561181,6490813651554920531,262144 --variations-seed-version=20260222-030036.739000-production --trace-process-track-uuid=3190709238376128875 --seatbelt-client=159
username          1034   0.0  0.6 469478128  93680   ??  S    Mon12PM   0:05.60 /Applications/Discord.app/Contents/Frameworks/Discord Helper (GPU).app/Contents/MacOS/Discord Helper (GPU) --type=gpu-process --user-data-dir=/Users/username/Library/Application Support/discord --gpu-preferences=UAAAAAAAAAAgAAAEAAAAAAAAAAAAAAAAAABgAAMAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --field-trial-handle=1718379636,r,14058496808204291326,15290222828867150131,262144 --enable-features=ScreenCaptureKitPickerScreen,ScreenCaptureKitStreamPickerSonoma --disable-features=AllowAggressiveThrottlingWithWebSocket,HardwareMediaKeyHandling,IntensiveWakeUpThrottling,MacWebContentsOcclusion,MediaSessionService,ScreenAIOCREnabled,SpareRendererForSitePerProcess,TimeoutHangingVideoCaptureStarts,UseEcoQoSForBackgroundProcess,WinRetrieveSuggestionsOnlyOnDemand --variations-seed-version --seatbelt-client=32
username           649   0.0  0.6 436006752 105920   ??  S    Mon12PM   0:06.80 /System/Applications/Notes.app/Contents/MacOS/Notes
_windowserver      411   0.0  0.6 435784784 104768   ??  Ss   Mon12PM   9:21.17 /System/Library/PrivateFrameworks/SkyLight.framework/Resources/WindowServer -daemon
username         15713   0.0  0.5 486085728  87648   ??  S     9:27AM   0:01.09 /Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/145.0.7632.109/Helpers/Google Chrome Helper (Alerts).app/Contents/MacOS/Google Chrome Helper (Alerts) --type=utility --utility-sub-type=mac_notifications.mojom.MacNotificationProvider --lang=ja --service-sandbox-type=none --message-loop-type-ui --shared-files --metrics-shmem-handle=1752395122,r,7600965871101911936,3481376327064934229,524288 --field-trial-handle=1718379636,r,14975098752248561181,6490813651554920531,262144 --variations-seed-version=20260222-030036.739000-production --trace-process-track-uuid=3190709194335161972
username          3116   0.0  0.5 435768576  81856   ??  Ss   Mon12PM   0:01.27 /System/Library/Frameworks/AppKit.framework/Versions/C/XPCServices/com.apple.appkit.xpc.openAndSavePanelService.xpc/Contents/MacOS/com.apple.appkit.xpc.openAndSavePanelService
username           723   0.0  0.5 469380000  77072   ??  S    Mon12PM   3:21.47 /Applications/Postman.app/Contents/Frameworks/Postman Helper (GPU).app/Contents/MacOS/Postman Helper (GPU) --type=gpu-process --user-data-dir=/Users/username/Library/Application Support/Postman --gpu-preferences=UAAAAAAAAAAgAAAEAAAAAAAAAAAAAAAAAABgAAEAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --field-trial-handle=1718379636,r,5079896452471728040,2752563536170496506,262144 --enable-features=ScreenCaptureKitPickerScreen,ScreenCaptureKitStreamPickerSonoma --disable-features=MacWebContentsOcclusion,SpareRendererForSitePerProcess,TimeoutHangingVideoCaptureStarts --variations-seed-version --seatbelt-client=34
username           708   0.0  0.5 435832144  75648   ??  S    Mon12PM   0:05.58 /System/Library/CoreServices/NotificationCenter.app/Contents/MacOS/NotificationCenter
username           651   0.0  0.5 435689040  77216   ??  S    Mon12PM   1:53.61 /System/Library/CoreServices/ControlCenter.app/Contents/MacOS/ControlCenter
root             15529   0.0  0.5 435387056  82496   ??  Ss    9:18AM   0:06.70 /usr/sbin/spindump
_mds_stores        558   0.0  0.5 442484816  90080   ??  Ss   Mon12PM   9:31.01 /System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/Metadata.framework/Versions/A/Support/mds_stores
username          3975   0.0  0.4 486099168  73824   ??  S    Mon12PM   0:03.64 /Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/145.0.7632.109/Helpers/Google Chrome Helper.app/Contents/MacOS/Google Chrome Helper --type=utility --utility-sub-type=video_capture.mojom.VideoCaptureService --lang=ja --service-sandbox-type=none --message-loop-type-ui --shared-files --metrics-shmem-handle=1752395122,r,15860076437827116901,8990417518384398629,524288 --field-trial-handle=1718379636,r,14975098752248561181,6490813651554920531,262144 --variations-seed-version=20260222-030036.739000-production --trace-process-track-uuid=3190709020045378058
username          3974   0.0  0.4 486073040  69184   ??  S    Mon12PM   0:08.77 /Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/145.0.7632.109/Helpers/Google Chrome Helper.app/Contents/MacOS/Google Chrome Helper --type=utility --utility-sub-type=audio.mojom.AudioService --lang=ja --service-sandbox-type=audio --message-loop-type-ui --shared-files --metrics-shmem-handle=1752395122,r,11108860393086703561,15731103217784825970,524288 --field-trial-handle=1718379636,r,14975098752248561181,6490813651554920531,262144 --variations-seed-version=20260222-030036.739000-production --trace-process-track-uuid=3190709019108336209 --seatbelt-client=185
username          3170   0.0  0.4 435875280  68768   ??  S    Mon12PM   0:01.06 /System/Library/CoreServices/UserNotificationCenter.app/Contents/MacOS/UserNotificationCenter
username          1421   0.0  0.4 435717200  62960   ??  Ss   Mon12PM   0:01.67 /System/Library/CoreServices/Dock.app/Contents/XPCServices/DockHelper.xpc/Contents/MacOS/DockHelper
username           900   0.0  0.4 435756160  71504   ??  S    Mon12PM   0:00.51 /System/Library/Services/AppleSpell.service/Contents/MacOS/AppleSpell
username           797   0.0  0.4 486066912  67296   ??  S    Mon12PM   0:02.25 /Applications/Google Chrome.app/Contents/Frameworks/Google Chrome Framework.framework/Versions/145.0.7632.109/Helpers/Google Chrome Helper.app/Contents/MacOS/Google Chrome Helper --type=utility --utility-sub-type=storage.mojom.StorageService --lang=ja --service-sandbox-type=service --shared-files --metrics-shmem-handle=1752395122,r,5890139135696665358,14767421606346415934,524288 --field-trial-handle=1718379636,r,14975098752248561181,6490813651554920531,262144 --variations-seed-version=20260222-030036.739000-production --trace-process-track-uuid=3190708990060038890 --seatbelt-client=28
username           765   0.0  0.4 435405840  63376   ??  Ss   Mon12PM   0:01.40 /System/Library/CoreServices/Dock.app/Contents/XPCServices/com.apple.dock.extra.xpc/Contents/MacOS/com.apple.dock.extra
username           716   0.0  0.4 435410400  63264   ??  S    Mon12PM   2:15.59 /usr/libexec/duetexpertd
username           658   0.0  0.4 435677792  63200   ??  S    Mon12PM   0:06.22 /System/Library/CoreServices/Finder.app/Contents/MacOS/Finder
_softwareupdate    568   0.0  0.4 439826080  69984   ??  Ss   Mon12PM   0:10.22 /System/Library/CoreServices/Software Update.app/Contents/Resources/softwareupdated
username         18086   0.0  0.3 440001568  49200   ??  S    12:21PM   0:00.29 /System/Library/PrivateFrameworks/Noticeboard.framework/Versions/A/Resources/nbagent.app/Contents/MacOS/nbagent
username         15028   0.0  0.3 436165824  42304   ??  S     8:41AM   0:00.30 openclaw    
username         12303   0.0  0.3 507450768  57760   ??  Ss    8:33AM   0:00.39 /System/Library/Frameworks/WebKit.framework/Versions/A/XPCServices/com.apple.WebKit.WebContent.xpc/Contents/MacOS/com.apple.WebKit.WebContent
username          1063   0.0  0.3 469242800  47472   ??  S    Mon12PM   0:02.92 /Applications/Discord.app/Contents/Frameworks/Discord Helper (Plugin).app/Contents/MacOS/Discord Helper (Plugin) --type=utility --utility-sub-type=video_capture.mojom.VideoCaptureService --lang=en-US --service-sandbox-type=none --message-loop-type-ui --user-data-dir=/Users/username/Library/Application Support/discord --standard-schemes=disclip --secure-schemes=disclip,sentry-ipc --bypasscsp-schemes=sentry-ipc --cors-schemes=sentry-ipc --fetch-schemes=disclip,sentry-ipc --streaming-schemes=disclip --shared-files --field-trial-handle=1718379636,r,14058496808204291326,15290222828867150131,262144 --enable-features=ScreenCaptureKitPickerScreen,ScreenCaptureKitStreamPickerSonoma --disable-features=AllowAggressiveThrottlingWithWebSocket,HardwareMediaKeyHandling,IntensiveWakeUpThrottling,MacWebContentsOcclusion,MediaSessionService,ScreenAIOCREnabled,SpareRendererForSitePerProcess,TimeoutHangingVideoCaptureStarts,UseEcoQoSForBackgroundProcess,WinRetrieveSuggestionsOnlyOnDemand --variations-seed-version
username          1036   0.0  0.3 469272368  57328   ??  S    Mon12PM   0:11.37 /Applications/Discord.app/Contents/Frameworks/Discord Helper.app/Contents/MacOS/Discord Helper --type=utility --utility-sub-type=network.mojom.NetworkService --lang=en-US --service-sandbox-type=network --user-data-dir=/Users/username/Library/Application Support/discord --standard-schemes=disclip --secure-schemes=disclip,sentry-ipc --bypasscsp-schemes=sentry-ipc --cors-schemes=sentry-ipc --fetch-schemes=disclip,sentry-ipc --streaming-schemes=disclip --shared-files --field-trial-handle=1718379636,r,14058496808204291326,15290222828867150131,262144 --enable-features=ScreenCaptureKitPickerScreen,ScreenCaptureKitStreamPickerSonoma --disable-features=AllowAggressiveThrottlingWithWebSocket,HardwareMediaKeyHandling,IntensiveWakeUpThrottling,MacWebContentsOcclusion,MediaSessionService,ScreenAIOCREnabled,SpareRendererForSitePerProcess,TimeoutHangingVideoCaptureStarts,UseEcoQoSForBackgroundProcess,WinRetrieveSuggestionsOnlyOnDemand --variations-seed-version --seatbelt-client=32
username           879   0.0  0.3 435610912  57216   ??  S    Mon12PM   0:01.01 /System/Library/CoreServices/TextInputMenuAgent.app/Contents/MacOS/TextInputMenuAgent
username           836   0.0  0.3 435432448  47200   ??  S    Mon12PM   0:07.66 /System/Library/PrivateFrameworks/PhotoAnalysis.framework/Versions/A/Support/photoanalysisd
username           829   0.0  0.3 435889072  45488   ??  S    Mon12PM   0:10.02 /System/Library/Frameworks/CoreSpotlight.framework/spotlightknowledged -u
username           783   0.0  0.3 439817408  46544   ??  S    Mon12PM   0:03.54 /System/Library/PrivateFrameworks/AppleMediaServicesUI.framework/amsengagementd
username           756   0.0  0.3 435539440  43008   ??  S    Mon12PM   0:00.47 /System/Library/PrivateFrameworks/AppSSO.framework/Support/AppSSOAgent.app/Contents/MacOS/AppSSOAgent
username           732   0.0  0.3 435377696  46288   ??  S    Mon12PM   0:01.92 /System/Library/PrivateFrameworks/HomeKitDaemon.framework/Support/homed
username           726   0.0  0.3 469271488  43472   ??  S    Mon12PM   0:16.63 /Applications/Postman.app/Contents/Frameworks/Postman Helper.app/Contents/MacOS/Postman Helper --type=utility --utility-sub-type=network.mojom.NetworkService --lang=en-US --service-sandbox-type=network --user-data-dir=/Users/username/Library/Application Support/Postman --shared-files --field-trial-handle=1718379636,r,5079896452471728040,2752563536170496506,262144 --enable-features=ScreenCaptureKitPickerScreen,ScreenCaptureKitStreamPickerSonoma --disable-features=MacWebContentsOcclusion,SpareRendererForSitePerProcess,TimeoutHangingVideoCaptureStarts --variations-seed-version --seatbelt-client=34
username           664   0.0  0.3 435609200  53472   ??  S    Mon12PM   0:00.66 /System/Library/CoreServices/AccessibilityUIServer.app/Contents/MacOS/AccessibilityUIServer
username           655   0.0  0.3 435539360  43008   ??  S    Mon12PM   0:00.69 /System/Library/CoreServices/SystemUIServer.app/Contents/MacOS/SystemUIServer
username           648   0.0  0.3 435395216  57904   ??  S    Mon12PM   0:17.67 /usr/libexec/sharingd
username           642   0.0  0.3 435546544  43424   ??  S    Mon12PM   0:00.48 /System/Library/CoreServices/CoreLocationAgent.app/Contents/MacOS/CoreLocationAgent
username           604   0.0  0.3 435622912  43280   ??  S    Mon12PM   0:02.83 /System/Library/CoreServices/CoreServicesUIAgent.app/Contents/MacOS/CoreServicesUIAgent
root              2812   0.0  0.3 436728144  43376   ??  Ss   Mon12PM   0:22.15 /opt/homebrew/opt/tailscale/bin/tailscaled
root               432   0.0  0.3 435367296  48208   ??  Ss   Mon12PM   0:31.75 /usr/libexec/mobileassetd
root               359   0.0  0.3 435377248  47520   ??  Ss   Mon12PM   0:45.20 /System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/Metadata.framework/Versions/A/Support/mds
root               330   0.3  0.3 435490224  53392   ??  Ss   Mon12PM   1:06.36 /usr/libexec/logd
_driverkit         523   0.7  0.3 435304960  42928   ??  Ss   Mon12PM   3:57.71 /System/Library/DriverExtensions/com.apple.DriverKit-AppleBCMWLAN.dext/com.apple.DriverKit-AppleBCMWLAN com.apple.bcmwlan 0x100000ce2 com.apple.DriverKit-AppleBCMWLAN
_coreaudiod        412   0.0  0.3 435381296  49904   ??  Ss   Mon12PM   1:20.26 /usr/sbin/coreaudiod
username         19658   0.0  0.2 435374464  26400   ??  S     1:54PM   0:00.10 /System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/Metadata.framework/Versions/A/Support/mdworker_shared -s mdworker -c MDSImporterWorker -m com.apple.mdworker.shared
username         17091   0.0  0.2 507347648  38576   ??  Ss   11:10AM   0:00.08 /System/Library/Frameworks/WebKit.framework/Versions/A/XPCServices/com.apple.WebKit.WebContent.xpc/Contents/MacOS/com.apple.WebKit.WebContent
username         11296   0.0  0.2 435376608  27488   ??  S     2:52AM   0:01.08 /usr/libexec/remindd
username         10877   0.0  0.2 435397504  29152   ??  S    12:27AM   0:00.78 /System/Library/PrivateFrameworks/AMPLibrary.framework/Versions/A/Support/AMPLibraryAgent --launchd
username         10182   0.0  0.2 435568912  26848   ??  Ss    5:44PM   0:00.10 /System/Library/CoreServices/ControlCenter.app/Contents/PlugIns/DisplayControls.appex/Contents/MacOS/DisplayControls -LaunchArguments eyJzZXJ2aWNlTmFtZSI6ImNvbS5hcHBsZS5jb250cm9scy5kaXNwbGF5IiwidHlwZSI6MSwiZW5oYW5jZWRTZWN1cml0eSI6ZmFsc2V9
username          4484   0.0  0.2 435410144  25440   ??  S    Mon12PM   0:00.48 /usr/libexec/studentd
username          4009   0.0  0.2 435415728  32560   ??  Ss   Mon12PM   0:00.81 /System/Library/Frameworks/Metal.framework/Versions/A/XPCServices/MTLCompilerService.xpc/Contents/MacOS/MTLCompilerService
username          3103   0.0  0.2 439973120  38096   ??  Ss   Mon12PM   0:02.23 /System/Library/Frameworks/WebKit.framework/Versions/A/XPCServices/com.apple.WebKit.GPU.xpc/Contents/MacOS/com.apple.WebKit.GPU
username          3102   0.0  0.2 439737376  27248   ??  Ss   Mon12PM   0:03.34 /System/Library/Frameworks/WebKit.framework/Versions/A/XPCServices/com.apple.WebKit.Networking.xpc/Contents/MacOS/com.apple.WebKit.Networking
username          3098   0.0  0.2 435366784  25376   ??  S    Mon12PM   0:00.63 /System/Library/PrivateFrameworks/PassKitCore.framework/passd
username          2035   0.0  0.2 435377296  33760   ??  S    Mon12PM   0:44.18 /System/Library/PrivateFrameworks/SafariSafeBrowsing.framework/com.apple.Safari.SafeBrowsing.Service
username          1623   0.0  0.2 435434272  26384   ??  S    Mon12PM   0:01.38 /System/Library/PrivateFrameworks/SkyLight.framework//Versions/A/Resources/AquaAppearanceHelper.app/Contents/MacOS/AquaAppearanceHelper
username          1586   0.0  0.2 435372576  25584   ??  S    Mon12PM   0:02.65 /usr/libexec/tipsd
username          1430   0.0  0.2 435458384  33120   ??  Ss   Mon12PM   0:00.78 /System/Library/PrivateFrameworks/SafariPlatformSupport.framework/Versions/A/XPCServices/com.apple.SafariPlatformSupport.Helper.xpc/Contents/MacOS/com.apple.SafariPlatformSupport.Helper
username          1177   0.0  0.2 435458544  32992   ??  Ss   Mon12PM   0:00.77 /System/Library/PrivateFrameworks/SafariPlatformSupport.framework/Versions/A/XPCServices/com.apple.SafariPlatformSupport.Helper.xpc/Contents/MacOS/com.apple.SafariPlatformSupport.Helper

## launchctl suspicious grep
PID	Status	Label
643	0	application.com.mitchellh.ghostty.651500.651506
-	0	com.ollama.ollama
-	0	com.openssh.ssh-agent
11335	0	com.hnc.Discord.ShipIt
1005	0	application.com.hnc.Discord.2842425.2842431
633	0	application.com.postmanlabs.mac.2593614.2593621

## user startup items
44:48: execution error: System Eventsでエラーが起きました: AppleEventがタイムアウトしました。 (-1712)

## SSH config quick
Include /etc/ssh/sshd_config.d/*
AuthorizedKeysFile	.ssh/authorized_keys
Subsystem	sftp	/usr/libexec/sftp-server
total 8
drwx------@  3 username  staff    96 Feb  3 18:59 .
drwxr-x---+ 39 username  staff  1248 Feb 24 11:12 ..
-rw-r--r--@  1 username  staff    92 Feb  3 18:59 known_hosts

## TCC / Full disk access grants (metadata only)
Error: unable to open database "/Users/username/Library/Application Support/com.apple.TCC/TCC.db": authorization denied

## Quarantine disabled flags check
LSQuarantine key not set (default on)
assessments enabled
