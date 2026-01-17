import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../App";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Input } from "../components/ui/input";
import { toast } from "sonner";
import { ArrowLeft, ShoppingCart, Minus, Plus, Package, Truck, Shield } from "lucide-react";

export default function ProductDetail() {
  const { productId } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);

  useEffect(() => {
    fetchProduct();
  }, [productId]);

  const fetchProduct = async () => {
    try {
      const response = await api.get(`/products/${productId}`);
      setProduct(response.data);
    } catch (error) {
      console.error("Error fetching product:", error);
    } finally {
      setLoading(false);
    }
  };

  const addToCart = async () => {
    try {
      await api.post("/cart/add", { product_id: productId, quantity });
      toast.success(`Added ${quantity} item(s) to cart!`);
    } catch (error) {
      toast.error("Failed to add to cart");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50">
        <Navbar />
        <div className="flex items-center justify-center py-20">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen bg-slate-50">
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 py-12 text-center">
          <h1 className="text-2xl font-bold text-slate-900 mb-4">Product not found</h1>
          <Link to="/shop">
            <Button variant="outline" className="rounded-sm">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Shop
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50" data-testid="product-detail">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Link to="/shop" className="inline-flex items-center text-slate-600 hover:text-slate-900 mb-6 transition-colors">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Shop
        </Link>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Image */}
          <div className="aspect-square bg-white border border-slate-200 rounded-sm overflow-hidden">
            <img
              src={product.image_url}
              alt={product.name}
              className="w-full h-full object-cover"
            />
          </div>

          {/* Details */}
          <div className="space-y-6">
            <div>
              <Badge variant="outline" className="mb-2">{product.category}</Badge>
              <h1 className="text-3xl font-bold text-slate-900 font-['Oswald'] uppercase tracking-tight mb-2">
                {product.name}
              </h1>
              <p className="text-sm text-slate-500">SKU: {product.sku}</p>
            </div>

            <div className="flex items-baseline gap-3">
              <span className="text-3xl font-bold text-slate-900">
                ${product.price.toFixed(2)}
              </span>
              {product.compare_price && product.compare_price > product.price && (
                <>
                  <span className="text-xl text-slate-400 line-through">
                    ${product.compare_price.toFixed(2)}
                  </span>
                  <Badge className="bg-orange-500 text-white">
                    Save ${(product.compare_price - product.price).toFixed(2)}
                  </Badge>
                </>
              )}
            </div>

            <p className="text-slate-600">{product.description}</p>

            <div className="flex items-center gap-2">
              {product.stock > 0 ? (
                <Badge className="status-active">In Stock ({product.stock} available)</Badge>
              ) : (
                <Badge variant="destructive">Out of Stock</Badge>
              )}
            </div>

            {/* Quantity & Add to Cart */}
            <div className="flex items-center gap-4">
              <div className="flex items-center border border-slate-200 rounded-sm">
                <Button
                  variant="ghost"
                  size="icon"
                  className="rounded-none"
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  data-testid="qty-decrease"
                >
                  <Minus className="w-4 h-4" />
                </Button>
                <Input
                  type="number"
                  value={quantity}
                  onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                  className="w-16 text-center border-0 rounded-none"
                  min="1"
                  max={product.stock}
                  data-testid="qty-input"
                />
                <Button
                  variant="ghost"
                  size="icon"
                  className="rounded-none"
                  onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                  data-testid="qty-increase"
                >
                  <Plus className="w-4 h-4" />
                </Button>
              </div>
              <Button
                onClick={addToCart}
                className="flex-1 bg-orange-500 hover:bg-orange-600 text-white rounded-sm py-6"
                disabled={product.stock === 0}
                data-testid="add-to-cart"
              >
                <ShoppingCart className="w-5 h-5 mr-2" />
                Add to Cart
              </Button>
            </div>

            {/* Features */}
            <div className="grid grid-cols-3 gap-4 pt-6 border-t border-slate-200">
              <div className="text-center">
                <Package className="w-6 h-6 mx-auto text-slate-400 mb-2" />
                <p className="text-xs text-slate-600">Professional Grade</p>
              </div>
              <div className="text-center">
                <Truck className="w-6 h-6 mx-auto text-slate-400 mb-2" />
                <p className="text-xs text-slate-600">Fast Shipping</p>
              </div>
              <div className="text-center">
                <Shield className="w-6 h-6 mx-auto text-slate-400 mb-2" />
                <p className="text-xs text-slate-600">Quality Guaranteed</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}
