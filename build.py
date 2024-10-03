import os
import json
import hashlib

css_styles = """
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css'); /* 引入FontAwesome */

body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Roboto', sans-serif;
  background-color: #fefcff; /* 使用更浅的主题色 */
  color: #333333;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  align-items: center;
  justify-content: center;
}

.header {
  text-align: center;
  padding: 40px 20px 20px;
  background-color: #e891f5; /* 主色调 */
  color: #ffffff;
  border-radius: 10px 10px 0 0;
}

.header h1 {
  font-size: 3em;
  font-weight: 700;
  margin: 0;
  line-height: 1.2;
}

.subheader {
  color: #ffffff;
  font-size: 1.1em;
  margin-top: 10px;
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  margin: 20px auto;
  padding: 20px;
  max-width: 800px;
  width: 90%;
  border: 1px solid #e16df2;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
}

a {
  color: #e16df2;
  text-decoration: none;
  transition: color 0.3s ease, transform 0.3s ease;
}

a:hover {
  color: #d226eb;
  transform: scale(1.05);
}

.info {
  margin-bottom: 20px;
  background: #f3c7fa;
  line-height: 1.8;
  font-size: 1.1em;
  text-align: left;
  width: 100%;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.current-path {
  margin-bottom: 20px;
  color: #666666;
  font-size: 1em;
  text-align: left;
  width: 100%;
}

ul {
  list-style: none;
  padding: 0;
  width: 100%;
}

ul li {
  margin-bottom: 10px;
  border: 1px solid #e1e1e1;
  border-radius: 5px;
  padding: 10px;
  background-color: #f6f6f6;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

ul li:hover {
  transform: scale(1.02);
  background-color: #efb5f8;
}

ul li a {
  color: #e16df2;
  transition: color 0.3s ease;
}

ul li a:hover {
  color: #d226eb;
}

.footer {
  text-align: center;
  padding: 20px;
  font-size: 1em;
  color: #aaaaaa; /* 修改为淡灰色 */
  margin-top: 40px;
}

.loading-bar {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background-color: #e891f5;
  width: 0;
  transition: width 0.5s ease-out;
}

@media (max-width: 768px) {
  .header h1 {
    font-size: 2.5em;
  }

  .content {
    padding: 15px;
  }
}
"""

# Update the HTML template for a list-based layout and new header structure
template = '''
<html>
    <head>
    <meta charset="utf-8">
    <title>AyameMC Maven Repo</title>
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <style>{css_styles}</style>
    <script>
        window.onload = function() {{
            document.querySelector(".loading-bar").style.width = "100%";
            setTimeout(function() {{
                document.querySelector(".loading-bar").style.opacity = "0";
            }}, 500);
        }};
    </script>
    </head>
    <body>
        <div class="loading-bar"></div>
        <div class="content">
            
            <div class="current-path">
                {current_path}
            </div>
            <ul>
                {content}
            </ul>
        </div>
        <div class="footer">
        AyameMC Maven Repo<br>
        Learn usage on <a href="https://docs.ayamemc.org/docs/dev-doc/intro/#%E9%85%8D%E7%BD%AE%E4%BE%9D%E8%B5%96" >Ayame Docs</a>.
      </div>
    </body>
</html>
'''

# 修改文件夹和文件模板以在名称前添加空心图标
dir_template = '<li><a href="{dir_name}/"><i class="far fa-folder"></i> {dir_name}/</a></li>'
file_template = '<li><a href="{file_name}"><i class="far fa-file"></i> {file_name}</a></li>'

def generate_index_html(root_dir):
    for root, dirs, files in os.walk(root_dir):
        # Ignore hidden folders and files
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]

        # 隐藏根目录的 build.py、build.sh 和 robots.txt 文件
        if root == root_dir:
            files = [f for f in files if f not in ['build.py', 'build.sh', 'robots.txt']]
            content = ''  # 初始化内容为空
        else:
            content = '<li><a href="../"><i class="fas fa-level-up-alt"></i> ../</a></li>'  # 在非根目录下显示返回上一级的链接

        # Generate current path information
        current_path = os.path.relpath(root, start=root_dir)
        current_path = current_path.replace('\\', '/')  # for Windows compatibility

        for dir_name in dirs:
            content += dir_template.format(dir_name=dir_name)  # 添加图标和斜杠
        for file_name in files:
            if file_name not in ['index.html', 'info.json', 'info.md']:
                content += file_template.format(file_name=file_name)  # 添加图标

        # Generate info.json
        info = {"files": [], "dirs": []}

        for file_name in files:
            if file_name not in ['index.html', 'info.json', 'info.md']:
                file_path = os.path.join(root, file_name)
                with open(file_path, 'rb') as f:
                    file_content = f.read()
                    sha256_hash = hashlib.sha256(file_content).hexdigest()
                    info["files"].append({"name": file_name, "sha256": sha256_hash})

        for dir_name in dirs:
            info["dirs"].append({"name": dir_name})

        with open(os.path.join(root, 'info.json'), 'w') as info_file:
            json.dump(info, info_file, indent=4)

        index_content = template.format(current_path=current_path, content=content, css_styles=css_styles)
        with open(os.path.join(root, 'index.html'), 'w') as f:
            f.write(index_content)

generate_index_html('.')
