//En la carpeta include se añaden todos los ficheros fuente que funcionan como cabecera (archivos .h o .hpp)
#ifndef EJEMPLO_CPP_REGULAR_POLYGON_HPP
#define EJEMPLO_CPP_REGULAR_POLYGON_HPP

namespace ejemplo_cpp
{
  class RegularPolygon
  {
    public:
      virtual void initialize(double side_length) = 0;
      virtual double area() = 0;
      virtual ~RegularPolygon(){}

    protected:
      RegularPolygon(){}
  };
}  // namespace ejemplo_cpp

#endif  // EJEMPLO_CPP_REGULAR_POLYGON_HPP