import * as React from 'react'

export interface TabsProps extends React.HTMLAttributes<HTMLDivElement> {
  defaultValue?: string
  value?: string
  onValueChange?: (value: string) => void
}

export const Tabs: React.ForwardRefExoticComponent<TabsProps & React.RefAttributes<HTMLDivElement>>
export const TabsList: React.ForwardRefExoticComponent<React.HTMLAttributes<HTMLDivElement> & React.RefAttributes<HTMLDivElement>>
export const TabsTrigger: React.ForwardRefExoticComponent<React.ButtonHTMLAttributes<HTMLButtonElement> & { value: string } & React.RefAttributes<HTMLButtonElement>>
export const TabsContent: React.ForwardRefExoticComponent<React.HTMLAttributes<HTMLDivElement> & { value: string } & React.RefAttributes<HTMLDivElement>>
