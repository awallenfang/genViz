#version 330

layout (location = 0) in vec3 aPos;
uniform mat4 transform;

uniform vec2 pos;


void main() {
    vec4 temp = transform * vec4(aPos.x, aPos.y, aPos.z, 1.0);
    gl_Position = vec4(temp.x + pos.x, temp.y + pos.y, temp.z, 1.);

}