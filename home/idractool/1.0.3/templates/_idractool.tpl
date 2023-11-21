{{- define "idractool.workload" -}}
workload:
  idractool:
    enabled: true
    primary: true
    type: Deployment
    podSpec:
      containers:
        idractool:
          enabled: true
          primary: true
          imageSelector: image
          securityContext:
            runAsUser: {{ .Values.runas.user }}
            runAsGroup: {{ .Values.runas.group }}
          env:
            HOST : {{ .Values.idracsetup.host }}
            PASSWORD_IDRAC : {{ .Values.idracsetup.password }}
            USER : {{ .Values.idracsetup.username }}
            MAIN_TOPIC : {{ .Values.mqttsetup.topic }}
            MQTT_HOST : {{ .Values.mqttsetup.host }}
            MQTT_USER : {{ .Values.mqttsetup.username }}
            MQTT_PASSWORD : {{ .Values.mqttsetup.password }}
            INTERVAL : {{ .Values.idracsetup.pythonlogging }}
            PYTHONUNBUFFERED : {{ .Values.idracsetup.pythonlogging }}
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
            readiness:
              enabled: false
            startup:
              enabled: false


      initContainers:
      {{- include "ix.v1.common.app.permissions" (dict "containerName" "01-permissions"
                                                        "UID" .Values.runas.user
                                                        "GID" .Values.runas.group
                                                        "mode" "check"
                                                        "type" "init") | nindent 8 }}

{{- end -}}
