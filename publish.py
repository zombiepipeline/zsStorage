import git
import os

commit = 'HEAD'
remote_name = 'origin'
branch_name = 'main'

studio = 'zombiestudio'
repo_path = os.path.dirname(os.path.dirname(__file__))
repo_path = os.path.join(repo_path, 'zsStorage')

repo = git.Repo(repo_path)
tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)

if len(tags) <= 0:
    tag_init = {"name": f"{studio}_2.0.0"}
    tags.append(tag_init)

versions = []
for tag in tags:
    version = list(map(lambda v: int(v), tag['name'].split('_')[1].split('.')))
    versions.append(version)

getVersion = versions[-1:][0]
v1 = getVersion[0]
v2 = getVersion[1]
v3 = getVersion[2]

currentVersion = [str(v1), str(v2), str(v3)]
currentVersion = ".".join(currentVersion)

if v3 >= 99:
    v2 += 1
    v3 = 0

if v2 >= 99:
    v1 += 1
v3 += 1

new_version = [str(v1), str(v2), str(v3)]
tag_name = "{}_{}".format(studio, ".".join(new_version))

if repo.is_dirty(untracked_files=True):
    try:
        repo.git.add(A=True)
        tag_message = 'Atualizando versao {}'.format(".".join(new_version))

        repo.index.commit(tag_message)
        remote = repo.remote(name=remote_name)
        push_info = remote.push(refspec=f'{branch_name}:{branch_name}')
        for info in push_info:
            if info.flags & info.ERROR:
                print(f'Erro ao fazer push: {info.summary}')
            else:
                print(f'Push realizado com sucesso: {info.summary}')

        print(f'Criando nova versao {tag_name}')
        new_tag = repo.create_tag(tag_name, ref=commit, message=tag_message)

        push_info_tags = remote.push(tags=True)
        for info in push_info_tags:
            if info.flags & info.ERROR:
                print(f'Erro ao fazer push da tag: {info.summary}')
            else:
                print(f'Push da tag realizado com sucesso: {info.summary}')

    except Exception as e:
        print(f'Ocorreu um erro ao realizar commit e push: {e}')
else:
    print(f'Nemhuma alteração para commit')
