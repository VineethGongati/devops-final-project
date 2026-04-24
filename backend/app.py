from flask import Flask, send_file, jsonify
import os
import datetime

app = Flask(__name__)

# ─── HTML Template ────────────────────────────────────────────────
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>DevOps Backend - MSIT 3404</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }

        body {
            font-family: system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f4c75 100%);
            min-height: 100vh;
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
        }

        .container { max-width: 680px; width: 100%; }

        @keyframes fadeUp {
            from { opacity:0; transform:translateY(20px); }
            to   { opacity:1; transform:translateY(0); }
        }
        @keyframes pulse { 0%,100%{transform:scale(1);} 50%{transform:scale(1.05);} }
        @keyframes blink  { 0%,100%{opacity:1;} 50%{opacity:0;} }

        .fade1 { animation: fadeUp .5s ease both; }
        .fade2 { animation: fadeUp .5s ease .1s both; }
        .fade3 { animation: fadeUp .5s ease .2s both; }
        .fade4 { animation: fadeUp .5s ease .3s both; }

        /* Top bar */
        .topbar {
            display:flex; align-items:center;
            justify-content:space-between; flex-wrap:wrap;
            gap:8px; margin-bottom:32px;
        }
        .dots { display:flex; gap:7px; align-items:center; }
        .dot { width:10px; height:10px; border-radius:50%; }
        .dot-r{background:#f87171;} .dot-y{background:#fbbf24;} .dot-g{background:#4ade80;}
        .path { font-size:12px; color:rgba(255,255,255,.4); margin-left:10px; font-family:monospace; }
        .tags { display:flex; gap:7px; flex-wrap:wrap; }
        .tag {
            font-size:11px; padding:3px 11px; border-radius:20px;
            background:rgba(255,255,255,.1); border:.5px solid rgba(255,255,255,.2);
            color:rgba(255,255,255,.8); display:inline-flex; align-items:center; gap:5px;
        }
        .live { width:7px; height:7px; border-radius:50%; background:#4ade80; animation:pulse 2s infinite; }

        /* Hero */
        .hero { text-align:center; margin-bottom:32px; }
        .icon { font-size:48px; animation:pulse 3s ease-in-out infinite; margin-bottom:10px; }
        h1 { font-size:30px; font-weight:600; letter-spacing:-.5px; margin-bottom:6px; }
        .sub { font-size:14px; color:rgba(255,255,255,.55); margin-bottom:16px; }

        /* Status badges */
        .badges { display:flex; justify-content:center; gap:8px; flex-wrap:wrap; margin-bottom:28px; }
        .badge {
            font-size:12px; font-weight:500; padding:5px 14px;
            border-radius:20px; display:inline-flex; align-items:center; gap:6px;
        }
        .b-green { background:rgba(74,222,128,.2); color:#86efac; border:.5px solid rgba(74,222,128,.3); }
        .b-blue  { background:rgba(99,102,241,.3); color:#c7d2fe; border:.5px solid rgba(99,102,241,.4); }
        .b-amber { background:rgba(251,191,36,.2); color:#fde68a; border:.5px solid rgba(251,191,36,.3); }

        /* Stats */
        .stats { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:24px; }
        .stat {
            background:rgba(255,255,255,.08); border:.5px solid rgba(255,255,255,.15);
            border-radius:12px; padding:14px 10px; text-align:center;
        }
        .stat-num { font-size:22px; font-weight:600; }
        .stat-lbl { font-size:11px; color:rgba(255,255,255,.5); margin-top:3px; }

        /* Routes */
        .section-label {
            font-size:10px; color:rgba(255,255,255,.35);
            text-transform:uppercase; letter-spacing:.08em; margin-bottom:10px;
        }
        .routes { display:flex; flex-direction:column; gap:8px; margin-bottom:24px; }
        .route {
            display:flex; align-items:center; gap:12px;
            background:rgba(255,255,255,.07); border:.5px solid rgba(255,255,255,.12);
            border-radius:10px; padding:12px 16px; text-decoration:none; color:#fff;
            transition: background .2s;
        }
        .route:hover { background:rgba(255,255,255,.13); }
        .method {
            font-size:11px; font-weight:600; padding:3px 9px; border-radius:6px;
            font-family:monospace; flex-shrink:0;
        }
        .get { background:rgba(74,222,128,.2); color:#86efac; }
        .route-path { font-family:monospace; font-size:13px; color:rgba(255,255,255,.85); }
        .route-desc { font-size:12px; color:rgba(255,255,255,.4); margin-left:auto; }
        .arrow { font-size:14px; color:rgba(255,255,255,.3); }

        /* Code block */
        .code-block {
            background:rgba(0,0,0,.35); border:.5px solid rgba(255,255,255,.1);
            border-radius:10px; padding:14px 16px; margin-bottom:20px;
            font-family:'Courier New',monospace; font-size:12px; line-height:1.8;
        }
        .kw{color:#f87171;} .fn{color:#86efac;} .st{color:#fde68a;} .cm{color:rgba(255,255,255,.3);}
        .cursor { display:inline-block; width:2px; height:12px; background:#fff; margin-left:2px; vertical-align:middle; animation:blink 1s infinite; }

        /* Footer */
        .footer { text-align:center; font-size:11px; color:rgba(255,255,255,.3); margin-top:20px; }
        .footer span { color:rgba(255,255,255,.6); }
    </style>
</head>
<body>
<div class="container">

    <div class="topbar fade1">
        <div style="display:flex;align-items:center;">
            <div class="dots">
                <div class="dot dot-r"></div>
                <div class="dot dot-y"></div>
                <div class="dot dot-g"></div>
            </div>
            <span class="path">devops-final-project / backend / app.py</span>
        </div>
        <div class="tags">
            <span class="tag"><span class="live"></span>running</span>
            <span class="tag">Flask 2.3.2</span>
            <span class="tag">port 5000</span>
        </div>
    </div>

    <div class="hero fade2">
        <div class="icon">&#9749;</div>
        <h1>Flask Backend API</h1>
        <p class="sub">DevOps Final Project &mdash; MSIT 3404</p>
        <div class="badges">
            <span class="badge b-green">&#10003; Server Online</span>
            <span class="badge b-blue">&#127981; Dockerized</span>
            <span class="badge b-amber">&#9729; Kubernetes Ready</span>
        </div>
    </div>

    <div class="stats fade3">
        <div class="stat">
            <div class="stat-num">3</div>
            <div class="stat-lbl">K8s replicas</div>
        </div>
        <div class="stat">
            <div class="stat-num">2</div>
            <div class="stat-lbl">API routes</div>
        </div>
        <div class="stat">
            <div class="stat-num" id="uptime">0s</div>
            <div class="stat-lbl">Uptime</div>
        </div>
    </div>

    <div class="fade4">
        <div class="section-label">Available routes</div>
        <div class="routes">
            <a href="/" class="route">
                <span class="method get">GET</span>
                <span class="route-path">/</span>
                <span class="route-desc">Home &mdash; this page</span>
                <span class="arrow">&#8594;</span>
            </a>
            <a href="/image" class="route">
                <span class="method get">GET</span>
                <span class="route-path">/image</span>
                <span class="route-desc">Display JPG image</span>
                <span class="arrow">&#8594;</span>
            </a>
            <a href="/health" class="route">
                <span class="method get">GET</span>
                <span class="route-path">/health</span>
                <span class="route-desc">Health check JSON</span>
                <span class="arrow">&#8594;</span>
            </a>
        </div>

        <div class="code-block">
            <div style="font-size:10px;color:rgba(255,255,255,.3);margin-bottom:6px;text-transform:uppercase;letter-spacing:.06em;">app.py</div>
            <div><span class="kw">from</span> flask <span class="kw">import</span> Flask, send_file, jsonify</div>
            <div><span class="fn">app</span> = Flask(__name__)</div>
            <div><span class="cm"># Routes: / &nbsp;/image &nbsp;/health</span></div>
            <div><span class="kw">app</span>.run(host=<span class="st">'0.0.0.0'</span>, port=<span class="st">5000</span>)<span class="cursor"></span></div>
        </div>
    </div>

    <div class="footer fade4">
        Team: <span>Vineeth Gongati</span> &mdash; MSIT 3404 DevOps &mdash;
        Due <span>May 4, 2026</span>
    </div>
</div>

<script>
    const start = Date.now();
    function updateUptime() {
        const s = Math.floor((Date.now() - start) / 1000);
        const el = document.getElementById('uptime');
        if (!el) return;
        if (s < 60) el.textContent = s + 's';
        else if (s < 3600) el.textContent = Math.floor(s/60) + 'm ' + (s%60) + 's';
        else el.textContent = Math.floor(s/3600) + 'h ' + Math.floor((s%3600)/60) + 'm';
    }
    setInterval(updateUptime, 1000);
    updateUptime();
</script>
</body>
</html>
"""

# ─── Routes ───────────────────────────────────────────────────────

@app.route('/')
def home():
    return HTML

@app.route('/image')
def display_image():
    for file in os.listdir('.'):
        if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
            return send_file(file, mimetype='image/jpeg')
    return '''
        <div style="text-align:center;font-family:system-ui;padding:60px;
                    background:#0f172a;color:#fff;min-height:100vh;">
            <h2 style="color:#f87171;">&#9888; No JPG found</h2>
            <p style="color:rgba(255,255,255,.5);margin-top:12px;">
                Add a .jpg file to the backend directory and restart Flask.
            </p>
        </div>
    '''

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "flask-backend",
        "course": "MSIT 3404 DevOps",
        "port": 5000,
        "timestamp": datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)