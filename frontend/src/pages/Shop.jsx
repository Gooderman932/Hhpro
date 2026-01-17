import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { api } from "../App";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Card, CardContent } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { toast } from "sonner";
import { Search, ShoppingCart, Tag, Package } from "lucide-react";

export default function Shop() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState("");

  useEffect(() => {
    fetchProducts();
    fetchCategories();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const params = (selectedCategory && selectedCategory !== "all") ? `?category=${selectedCategory}` : "";
      const response = await api.get(`/products${params}`);
      setProducts(response.data);
    } catch (error) {
      console.error("Error fetching products:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await api.get("/product-categories");
      setCategories(response.data);
    } catch (error) {
      console.error("Error fetching categories:", error);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, [selectedCategory]);

  const addToCart = async (productId) => {
    try {
      await api.post("/cart/add", { product_id: productId, quantity: 1 });
      toast.success("Added to cart!");
    } catch (error) {
      toast.error("Failed to add to cart");
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      
      {/* Header */}
      <div className="bg-slate-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl md:text-4xl font-bold font-['Oswald'] uppercase tracking-tight mb-2">
            Pro Shop
          </h1>
          <p className="text-slate-400">
            Professional-grade tools and supplies for contractors
          </p>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white border-b border-slate-200 py-4 sticky top-16 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row gap-4 items-center">
            <Select
              value={selectedCategory}
              onValueChange={setSelectedCategory}
            >
              <SelectTrigger className="md:w-64 rounded-sm" data-testid="category-filter">
                <SelectValue placeholder="All Categories" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                {categories.map((cat) => (
                  <SelectItem key={cat} value={cat}>{cat}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Link to="/cart" className="ml-auto">
              <Button variant="outline" className="rounded-sm" data-testid="view-cart-btn">
                <ShoppingCart className="w-4 h-4 mr-2" />
                View Cart
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Products Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-6">
          <p className="text-slate-600">
            {loading ? "Loading..." : `${products.length} products`}
          </p>
        </div>

        {loading ? (
          <div className="flex justify-center py-12">
            <div className="spinner"></div>
          </div>
        ) : products.length === 0 ? (
          <Card className="border border-slate-200 rounded-sm">
            <CardContent className="py-12 text-center">
              <Package className="w-12 h-12 text-slate-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-slate-900 mb-2">No products found</h3>
              <p className="text-slate-600">Check back soon for new inventory</p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {products.map((product) => (
              <Card 
                key={product.product_id} 
                className="product-card border border-slate-200 rounded-sm overflow-hidden group"
                data-testid={`product-card-${product.product_id}`}
              >
                <div className="aspect-square bg-slate-100 relative overflow-hidden">
                  <img
                    src={product.image_url}
                    alt={product.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  {product.compare_price && product.compare_price > product.price && (
                    <Badge className="absolute top-2 left-2 bg-orange-500 text-white rounded-sm">
                      Sale
                    </Badge>
                  )}
                  {product.stock < 10 && product.stock > 0 && (
                    <Badge variant="secondary" className="absolute top-2 right-2 rounded-sm">
                      Low Stock
                    </Badge>
                  )}
                </div>
                <CardContent className="p-4">
                  <Badge variant="outline" className="text-xs mb-2">{product.category}</Badge>
                  <h3 className="font-semibold text-slate-900 mb-1 line-clamp-2">
                    {product.name}
                  </h3>
                  <div className="flex items-center gap-2 mb-3">
                    <span className="text-lg font-bold text-slate-900">
                      ${product.price.toFixed(2)}
                    </span>
                    {product.compare_price && product.compare_price > product.price && (
                      <span className="text-sm text-slate-400 line-through">
                        ${product.compare_price.toFixed(2)}
                      </span>
                    )}
                  </div>
                  <div className="flex gap-2">
                    <Button
                      onClick={() => addToCart(product.product_id)}
                      className="flex-1 bg-slate-900 hover:bg-slate-800 text-white rounded-sm text-sm"
                      disabled={product.stock === 0}
                      data-testid={`add-to-cart-${product.product_id}`}
                    >
                      <ShoppingCart className="w-4 h-4 mr-1" />
                      {product.stock === 0 ? "Out of Stock" : "Add"}
                    </Button>
                    <Link to={`/shop/${product.product_id}`}>
                      <Button variant="outline" className="rounded-sm text-sm">
                        View
                      </Button>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}
