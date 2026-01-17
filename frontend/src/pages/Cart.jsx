import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { api } from "../App";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Input } from "../components/ui/input";
import { toast } from "sonner";
import { ShoppingCart, Trash2, Minus, Plus, ArrowLeft, Loader2 } from "lucide-react";

export default function Cart() {
  const [cart, setCart] = useState({ items: [], subtotal: 0, item_count: 0 });
  const [loading, setLoading] = useState(true);
  const [checkoutLoading, setCheckoutLoading] = useState(false);

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      const response = await api.get("/cart");
      setCart(response.data);
    } catch (error) {
      console.error("Error fetching cart:", error);
    } finally {
      setLoading(false);
    }
  };

  const updateQuantity = async (productId, quantity) => {
    try {
      await api.post("/cart/update", { product_id: productId, quantity });
      fetchCart();
    } catch (error) {
      toast.error("Failed to update cart");
    }
  };

  const removeItem = async (productId) => {
    try {
      await api.delete(`/cart/${productId}`);
      fetchCart();
      toast.success("Item removed from cart");
    } catch (error) {
      toast.error("Failed to remove item");
    }
  };

  const clearCart = async () => {
    try {
      await api.delete("/cart");
      fetchCart();
      toast.success("Cart cleared");
    } catch (error) {
      toast.error("Failed to clear cart");
    }
  };

  const handleCheckout = async () => {
    if (cart.items.length === 0) {
      toast.error("Your cart is empty");
      return;
    }

    setCheckoutLoading(true);
    try {
      const response = await api.post("/checkout/create-session", {
        origin_url: window.location.origin
      });
      window.location.href = response.data.url;
    } catch (error) {
      toast.error(error.response?.data?.detail || "Failed to start checkout");
      setCheckoutLoading(false);
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

  return (
    <div className="min-h-screen bg-slate-50" data-testid="cart-page">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Link to="/shop" className="inline-flex items-center text-slate-600 hover:text-slate-900 mb-6 transition-colors">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Continue Shopping
        </Link>

        <h1 className="text-3xl font-bold text-slate-900 font-['Oswald'] uppercase tracking-tight mb-8">
          Shopping Cart
        </h1>

        {cart.items.length === 0 ? (
          <Card className="border border-slate-200 rounded-sm">
            <CardContent className="py-12 text-center">
              <ShoppingCart className="w-12 h-12 text-slate-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-slate-900 mb-2">Your cart is empty</h3>
              <p className="text-slate-600 mb-4">Add some items to get started</p>
              <Link to="/shop">
                <Button className="bg-orange-500 hover:bg-orange-600 text-white rounded-sm">
                  Browse Products
                </Button>
              </Link>
            </CardContent>
          </Card>
        ) : (
          <div className="grid md:grid-cols-3 gap-8">
            {/* Cart Items */}
            <div className="md:col-span-2 space-y-4">
              {cart.items.map((item) => (
                <Card key={item.product_id} className="border border-slate-200 rounded-sm" data-testid={`cart-item-${item.product_id}`}>
                  <CardContent className="p-4">
                    <div className="flex gap-4">
                      <div className="w-24 h-24 bg-slate-100 rounded-sm overflow-hidden flex-shrink-0">
                        <img
                          src={item.image_url}
                          alt={item.name}
                          className="w-full h-full object-cover"
                        />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-slate-900 truncate">{item.name}</h3>
                        <p className="text-lg font-bold text-slate-900 mt-1">
                          ${item.price.toFixed(2)}
                        </p>
                        <div className="flex items-center gap-4 mt-3">
                          <div className="flex items-center border border-slate-200 rounded-sm">
                            <Button
                              variant="ghost"
                              size="icon"
                              className="h-8 w-8 rounded-none"
                              onClick={() => updateQuantity(item.product_id, item.quantity - 1)}
                            >
                              <Minus className="w-3 h-3" />
                            </Button>
                            <span className="w-8 text-center text-sm">{item.quantity}</span>
                            <Button
                              variant="ghost"
                              size="icon"
                              className="h-8 w-8 rounded-none"
                              onClick={() => updateQuantity(item.product_id, item.quantity + 1)}
                            >
                              <Plus className="w-3 h-3" />
                            </Button>
                          </div>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="text-red-500 hover:text-red-600 hover:bg-red-50"
                            onClick={() => removeItem(item.product_id)}
                          >
                            <Trash2 className="w-4 h-4 mr-1" />
                            Remove
                          </Button>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold text-slate-900">
                          ${(item.price * item.quantity).toFixed(2)}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
              
              <Button
                variant="ghost"
                className="text-slate-600"
                onClick={clearCart}
                data-testid="clear-cart"
              >
                <Trash2 className="w-4 h-4 mr-2" />
                Clear Cart
              </Button>
            </div>

            {/* Order Summary */}
            <div>
              <Card className="border border-slate-200 rounded-sm sticky top-24">
                <CardHeader>
                  <CardTitle className="font-['Oswald'] uppercase tracking-tight">
                    Order Summary
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-600">Items ({cart.item_count})</span>
                    <span>${cart.subtotal.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-600">Shipping</span>
                    <span className="text-green-600">Calculated at checkout</span>
                  </div>
                  <div className="border-t border-slate-200 pt-4">
                    <div className="flex justify-between font-semibold text-lg">
                      <span>Subtotal</span>
                      <span>${cart.subtotal.toFixed(2)}</span>
                    </div>
                  </div>
                  <Button
                    onClick={handleCheckout}
                    className="w-full bg-orange-500 hover:bg-orange-600 text-white rounded-sm py-6"
                    disabled={checkoutLoading}
                    data-testid="checkout-btn"
                  >
                    {checkoutLoading ? (
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    ) : null}
                    Proceed to Checkout
                  </Button>
                  <p className="text-xs text-slate-500 text-center">
                    Secure checkout powered by Stripe
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
      </div>

      <Footer />
    </div>
  );
}
