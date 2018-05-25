#pragma once

#include <SFML/Graphics.hpp>

/**
    Cube class to draw each "cell" in the game of life
**/
class Cube : public sf::Drawable, public sf::Transformable
{
    public:
        Cube(unsigned int size);
        void setColor();
        bool draw_front;
        bool draw_back;
        bool draw_left;
        bool draw_right;
        bool draw_top;
        bool draw_bottom;

        // const sf::RenderWindow& getWindow() const;

    private:
        void draw();

        sf::VertexArray verts_front;
        sf::VertexArray verts_back;
        sf::VertexArray verts_left;
        sf::VertexArray verts_right;
        sf::VertexArray verts_top;
        sf::VertexArray verts_bottom;
        // sf::Texture m_texture;
};
