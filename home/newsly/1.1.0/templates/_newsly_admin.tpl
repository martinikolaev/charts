{{- define "newsly_admin.workload" -}}
workload:
  newsly-admin:
    enabled: true
    primary: false
    type: Deployment
    podSpec:
      hostNetwork: {{ .Values.newslyAdminNetwork.hostNetwork }}
      containers:
        newsly-admin:
          enabled: true
          primary: true
          imageSelector: image
          command: [ "flask" ]
          args: ["run", "--host=0.0.0.0", "--port={{ .Values.newslyAdminNetwork.webPort }}"]
          securityContext:
            runAsUser: {{ .Values.newslyRunAs.user }}
            runAsGroup: {{ .Values.newslyRunAs.group }}
          env:
            FLASK_APP: app-admin.py
            FLASK_RUN_PORT: {{ .Values.newslyAdminNetwork.webPort }}
            DBHOST : {{ .Values.newslyDatabase.host }}
            DBUSERNAME : {{ .Values.newslyDatabase.username }}
            DBPASSWORD : {{ .Values.newslyDatabase.password }}
            DBPORT : {{ .Values.newslyDatabase.port }}
            DBNAME : {{ .Values.newslyDatabase.dbname }}
            PYTHONUNBUFFERED : {{ .Values.newslyDatabase.pythonlogging }}
          {{ with .Values.newslyConfig.additionalEnvs }}
          envList:
            {{ range $env := . }}
            - name: {{ $env.name }}
              value: {{ $env.value }}
            {{ end }}
          {{ end }}
          probes:
            liveness:
              enabled: false
              type: http
              port: "{{ .Values.newslyAdminNetwork.webPort }}"
              path: /
              initialDelaySeconds: 5
              periodSeconds: 60
            readiness:
              enabled: false
              type: http
              port: "{{ .Values.newslyAdminNetwork.webPort }}"
              path: /
            startup:
              enabled: false
              type: http
              port: "{{ .Values.newslyAdminNetwork.webPort }}"
              path: /

{{/* Service */}}
service:
  newsly:
    enabled: true
    primary: true
    type: NodePort
    targetSelector: newsly
    ports:
      webui:
        enabled: true
        primary: true
        port: {{ .Values.newslyAdminNetwork.webPort }}
        nodePort: {{ .Values.newslyAdminNetwork.webPort }}
        targetSelector: newsly

{{- end -}}
