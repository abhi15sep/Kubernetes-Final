{{- define "imagePullSecret" }}
{{- printf "{\"auths\": {\"%s\": {\"auth\": \"%s\"}}}" .Values.privateRegistry.url (printf "%s:%s" .Values.privateRegistry.user .Values.privateRegistry.pass | b64enc) | b64enc }}
{{- end -}}
