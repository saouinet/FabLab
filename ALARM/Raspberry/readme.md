
# Description
contiend 
description des opérations d'installation du serveur
la liste des fichiers et dossiers du serveur raspberry

# Installation

## Installation d'une image Rasbian
 - configuration:
  - nom : raspi-poste(n)
  - pass : Burkert67
  - localisation
  - clavier en FR
  - activation de ssh
----
 - update et upgrade
----
## installation de Docker
 - curl -sSL get.docker.com | sh
----
## installation de rasp-ap
 - sauvegarde wpa_supplicant:
 
 "sudo cp /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf.org"
 
 - supression de la config wpa_supplicant:
 
 "sudo  rm  /etc/wpa_supplicant/wpa_supplicant.conf"
 
 - install rasp-ap:
 
 "wget -q https://git.io/voEUQ -O /tmp/raspap && bash /tmp/raspap"
 - admin
 - secret
 - hotspot:
  - wlan0
  - SSID raspi-poste1
  - pass Burkert67
  - canal 6
 "Masquer le SSID en diffusion" plus tard.
 
 ip du serveur : 10.141.3.1
----
 - installation de mosquitto
  - port mqtt: 1883
  - port websocket : 
----
- ajouter dossier RPi

- ajouter dossier back-end
