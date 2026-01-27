/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

// Declare UI component modules
declare module '*.jsx' {
  const content: any
  export default content
  export const Button: any
  export const Input: any
  export const Label: any
  export const Card: any
  export const CardHeader: any
  export const CardTitle: any
  export const CardDescription: any
  export const CardContent: any
  export const CardFooter: any
  export const Badge: any
  export const Tabs: any
  export const TabsList: any
  export const TabsTrigger: any
  export const TabsContent: any
}
