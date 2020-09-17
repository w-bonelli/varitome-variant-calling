import subprocess
import os

#Returns the directory that is mounted in the bio_c container
def get_mount_location():
    output = subprocess.check_output("docker inspect -f '{{ .Mounts }}' bio_c", shell=True).decode()
    mount_location = output.split(' ')[2]

    return(mount_location)


def restart_docker_container(mount_directory):
    subprocess.call("docker pull awilliams21/bioinformatics_assets", shell=True)
    subprocess.call("docker stop bio_c", shell=True)
    subprocess.call("docker rm bio_c", shell=True)
    subprocess.call("docker run -d -it --name bio_c --mount \
                    type=bind,source=%s,target=/bio \
                    awilliams21/bioinformatics_assets:latest" \
                    % (mount_directory), shell=True)
    subprocess.call("docker cp /usr/local/lib/TomatoGenomeFiles/BGV1.0_genome.fasta bio_c:/bio/BGV1.0_genome.fasta", shell=True)
    subprocess.call("docker cp /usr/local/lib/TomatoGenomeFiles/BGV1.0_genome.fasta bio_c:/bio/BGV1.0_genome.fasta.fai", shell=True)
    subprocess.call("docker cp /usr/local/lib/TomatoGenomeFiles/BGV1.0_genome.fasta bio_c:/bio/BGV1.0_genome.fasta.amb", shell=True)
    subprocess.call("docker cp /usr/local/lib/TomatoGenomeFiles/BGV1.0_genome.fasta bio_c:/bio/BGV1.0_genome.fasta.ann", shell=True)
    subprocess.call("docker cp /usr/local/lib/TomatoGenomeFiles/BGV1.0_genome.fasta bio_c:/bio/BGV1.0_genome.fasta.bwt", shell=True)
    return


def check_container_status(mount_directory):
    #Check the current mount location
    try:
        current_mount_location = get_mount_location()
    except:
        restart_docker_container(mount_directory)
        return

    #Clean up user input mount directory to match style of docker output
    if mount_directory.endswith('/'):
        mount_directory = mount_directory[0:-1]
    if not mount_directory.startswith('/'):
        mount_directory = '/' + mount_directory

    #Restarts bio_c with new mount directory
    if mount_directory == current_mount_location:
        isRunning = subprocess.check_output("docker inspect -f {{.State.Running}} \
                                            bio_c", shell=True).decode()[0:-1]
        if isRunning == "true":
            return

    restart_docker_container(mount_directory)

    return
