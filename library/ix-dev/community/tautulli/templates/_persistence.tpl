{{- define "tautulli.persistence" -}}
persistence:
  config:
    enabled: true
    type: {{ .Values.tautulliStorage.config.type }}
    datasetName: {{ .Values.tautulliStorage.config.datasetName | default "" }}
    hostPath: {{ .Values.tautulliStorage.config.hostPath | default "" }}
    targetSelector:
      tautulli:
        tautulli:
          mountPath: /config
        01-permissions:
          mountPath: /mnt/directories/config
  tmp:
    enabled: true
    type: emptyDir
    targetSelector:
      tautulli:
        tautulli:
          mountPath: /tmp
  {{- range $idx, $storage := .Values.tautulliStorage.additionalStorages }}
  {{ printf "tautulli-%v" (int $idx) }}:
    {{- $size := "" -}}
    {{- if $storage.size -}}
      {{- $size = (printf "%vGi" $storage.size) -}}
    {{- end }}
    enabled: true
    type: {{ $storage.type }}
    datasetName: {{ $storage.datasetName | default "" }}
    hostPath: {{ $storage.hostPath | default "" }}
    server: {{ $storage.server | default "" }}
    share: {{ $storage.share | default "" }}
    domain: {{ $storage.domain | default "" }}
    username: {{ $storage.username | default "" }}
    password: {{ $storage.password | default "" }}
    size: {{ $size }}
    {{- if eq $storage.type "smb-pv-pvc" }}
    mountOptions:
      - key: noperm
    {{- end }}
    targetSelector:
      tautulli:
        tautulli:
          mountPath: {{ $storage.mountPath }}
        01-permissions:
          mountPath: /mnt/directories{{ $storage.mountPath }}
  {{- end }}
{{- end -}}
