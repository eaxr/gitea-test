# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "centos/8"

  config.vm.provider "libvirt" do |vrt|
    vrt.cpu = "1"
    vrt.memory = "2048"
  end

  config.vm.define "nginx" do |nginx|
    nginx.vm.hostname = "nginx.gitea-test"
    nginx.vm.network "public_network", bridge: "template interface name"
    nginx.vm.provision :ansible do |ansible|
      ansible.playbook = "playbook_nginx_install.yaml"
    end
  end

  config.vm.define "gitea" do |gitea|
    gitea.vm.hostname = "gitea.gitea-test"
    gitea.vm.network "public_network", bridge: "template interface name"
    gitea.vm.provision :ansible do |ansible|
      ansible.playbook = "playbook_gitea_install.yaml"
    end
  end

  config.vm.define "postgresql" do |postgresql|
    postgresql.vm.hostname = "postgresql.gitea-test"
    postgresql.vm.network "public_network", bridge: "template interface name"
    postgresql.vm.provision :ansible do |ansible|
      ansible.playbook = "playbook_postgresql_install.yaml"
    end
  end

end