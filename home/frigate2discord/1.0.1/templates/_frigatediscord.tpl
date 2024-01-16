{{- define "frigate2discord.workload" -}}
workload:
  frigate2discord:
    enabled: true
    primary: true
    type: Deployment
    podSpec:
      hostNetwork: {{ .Values.network.hostNetwork }}
      containers:
        frigate2discord:
          enabled: true
          primary: true
          imageSelector: image
          securityContext:
            runAsUser: {{ .Values.runas.user }}
            runAsGroup: {{ .Values.runas.group }}
          env:
            MQTT_BROKER : {{ .Values.mqttsetup.host }}
            MQTT_TOPIC : {{ .Values.mqttsetup.password }}
            MQTT_USERNAME : {{ .Values.mqttsetup.username }}
            MQTT_PASSWORD : {{ .Values.mqttsetup.topic }}
            DISCORD_WEBHOOK_URL : {{ .Values.discordsetup.webhook }}
            BASE_URL : {{ .Values.basesetup.username }}
          {{ with .Values.toolConfig.additionalEnvs }}
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
              port: "{{ .Values.network.webPort }}"
              path: /init-scraper
              initialDelaySeconds: 5
              periodSeconds: 60
            readiness:
              enabled: false
              type: http
              port: "{{ .Values.network.webPort }}"
              path: /
            startup:
              enabled: false
              type: http
              port: "{{ .Values.network.webPort }}"
              path: /

      initContainers:
      {{- include "ix.v1.common.app.permissions" (dict "containerName" "01-permissions"
                                                        "UID" .Values.runas.user
                                                        "GID" .Values.runas.group
                                                        "mode" "check"
                                                        "type" "init") | nindent 8 }}

{{/* Service */}}
service:
  frigate2discord:
    enabled: true
    primary: true
    type: NodePort
    targetSelector: frigate2discord

{{- end -}}
