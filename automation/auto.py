from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os

# import requests

CONTAINERS_INFO = {
    'kali': {
        'image': 'kali_linux_image',
        'ram': 8
    },
    'rocky': {
        'image': 'rocky_linux_image',
        'ram': 4
    },
    'ubuntu': {
        'image': 'ubuntu_image',
        'ram': 4
    },
    'centos': {
        'image': 'centos_image',
        'ram': 4
    }
}

TEMPLATE = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {name}
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: {label}
  template:
    metadata:
      labels:
        app: {label}
    spec:
      containers:
      - name: {container_name}
        image: {image}
        ports:
            - containerPort: 80
        resources:
          limits:
            memory: "{ram}Gi"
"""

app = Flask(__name__)
CORS(app)  # 이 코드가 Flask 애플리케이션에 CORS를 적용합니다.

@app.route('/data', methods=['POST'])
@cross_origin()  # 이 데코레이터는 이 엔드포인트에 대해 CORS를 허용합니다.

def handle_data():
    # response = requests.get('http://172.30.5.73:80') # 데이터를 받는 경로 수정해야 할 수도 잇음, 
    # 내부일시 이줄 삭제
    # data = response.json() # JSON 데이터를 파이썬 딕셔너리로 변환합니다.
    data = request.get_json() # 내부일시 
    
    form_name = data.get('formName')
    
    if form_name == 'containerForm':
        # 첫 번째 컨테이너 폼에서 보낸 데이터를 처리하는 로직
        for container_name, container_info in CONTAINERS_INFO.items():
            count = int(data.get(container_name + 'Count'))
            yaml = TEMPLATE.format(
                name=f"{container_name}_deployment",
                replicas=count,
                label=container_name,
                container_name=f"{container_name}_container",
                image=container_info['image'],
                ram=container_info['ram']
            )
            
            # 파일 이름을 생성합니다.
            file_name = f"{container_name}_deployment.yaml"

            # 파일 경로를 생성합니다.
            folder_path = 'deployments'
            os.makedirs(folder_path, exist_ok=True)  # 폴더가 없으면 생성합니다.
            file_path = os.path.join(folder_path, file_name)
            
            # YAML 파일을 저장합니다.
            with open(file_path, 'w') as file:
                file.write(yaml)


    
    return jsonify({'message': 'Data received successfully'}), 200

if __name__ == "__main__":
    app.run(host='localhost', port=5001, debug=True)
