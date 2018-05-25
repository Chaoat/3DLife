#include "Cube.h"

Cube::Cube(unsigned int size) {
    draw_front = true;
    draw_back = true;
    draw_left = true;
    draw_right = true;
    draw_top = true;
    draw_bottom = true;

    // front face
    verts_front = sf::VertexArray(sf::Quads, 4);
    verts_front[0].position = sf::Vector3f(-size/2, -size/2, size/2); 
    verts_front[1].position = sf::Vector3f(size/2, -size/2, size/2); 
    verts_front[2].position = sf::Vector3f(size/2, size/2, size/2); 
    verts_front[3].position = sf::Vector3f(-size/2, size/2, size/2); 

    // back face
    verts_back = sf::VertexArray(sf::Quads, 4);
    verts_back[0].position = sf::Vector3f(-size/2, -size/2, -size/2); 
    verts_back[1].position = sf::Vector3f(size/2, -size/2, -size/2); 
    verts_back[2].position = sf::Vector3f(size/2, size/2, -size/2); 
    verts_back[3].position = sf::Vector3f(-size/2, size/2, -size/2); 
    
    // left face
    verts_left = sf::VertexArray(sf::Quads, 4);
    verts_left[0].position = sf::Vector3f(-size/2, size/2, -size/2); 
    verts_left[1].position = sf::Vector3f(-size/2, size/2, size/2); 
    verts_left[2].position = sf::Vector3f(-size/2, -size/2, size/2); 
    verts_left[3].position = sf::Vector3f(-size/2, -size/2, -size/2); 

    // right face
    verts_right = sf::VertexArray(sf::Quads, 4);
    verts_right[0].position = sf::Vector3f(size/2, size/2, -size/2); 
    verts_right[1].position = sf::Vector3f(size/2, size/2, size/2); 
    verts_right[2].position = sf::Vector3f(size/2, -size/2, size/2); 
    verts_right[3].position = sf::Vector3f(size/2, -size/2, -size/2); 

    // top face
    verts_top = sf::VertexArray(sf::Quads, 4);
    verts_top[0].position = sf::Vector3f(-size/2, size/2, size/2); 
    verts_top[1].position = sf::Vector3f(size/2, size/2, size/2); 
    verts_top[2].position = sf::Vector3f(size/2, size/2, -size/2); 
    verts_top[3].position = sf::Vector3f(-size/2, size/2, -size/2);

    // bottom face 
    verts_bottom = sf::VertexArray(sf::Quads, 4);
    verts_bottom[0].position = sf::Vector3f(-size/2, -size/2, size/2); 
    verts_bottom[1].position = sf::Vector3f(size/2, -size/2, size/2); 
    verts_bottom[2].position = sf::Vector3f(size/2, -size/2, -size/2); 
    verts_bottom[3].position = sf::Vector3f(-size/2, -size/2, -size/2);
}

virtual void Cube::draw(sf::RenderTarget& target, sf::RenderStates states) const
    {
        // apply the entity's transform -- combine it with the one that was passed by the caller
        states.transform *= getTransform(); // getTransform() is defined by sf::Transformable

        // apply the texture
        // states.texture = &m_texture;

        // you may also override states.shader or states.blendMode if you want

        // draw the visible vertex arrays
        if(draw_front) target.draw(verts_front, states);
        if(draw_back) target.draw(verts_back, states);
        if(draw_left) target.draw(verts_left, states);
        if(draw_right) target.draw(verts_right, states);
        if(draw_top) target.draw(verts_top, states);
        if(draw_bottom) target.draw(verts_bottom, states);
    }
};

void Cube::setColor(st::Color color)  {
    for( int i = 0; i < m_vertices.size(); i++ ) {
        m_vertices[i].color = color;
    }
}